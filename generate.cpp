#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fstream>
#include <iomanip>
#include <string>
#include <vector>
#include <map>

#define NO_INDENT false
#define INDENT true

const int LANG_ENG = 0, LANG_CHN = 1;
const bool MARKDOWN = true, RAW = false;
const int MAXD = 20, MAX_BUFF_LEN = 1024;

std::vector<std::string> category, category_nam;
std::vector<bool> appeared_new, appeared_old;
std::vector<std::pair<int, int>> changed;
std::vector<int> removed, newed;
std::map<std::string, int> low;
int language = LANG_ENG;
bool markdown = MARKDOWN;
bool eof;

class record {
public:
    record() {}
    void print(bool indent)
    {
        if (indent)
            printf("    ");
        printf("{\n");
        for (size_t i = 0; i < category.size(); ++i) {
            if (indent)
                printf("    ");
            printf("    %s: %s,\n",category[i].c_str(), data[i].c_str());
        }
        if (indent)
            printf("    ");
        printf("}\n");
    }
    std::string fullform(const std::string& s)
    {
        int i = low[s];
        std::string res = category_nam[i] + ": " + data[i] + "\n";
        return res;
    }
    std::string operator[] (const std::string &index)
    {
        return data[low[index]];
    }
    std::vector<std::string> data;
};

bool operator==(const std::vector<std::string>& a, const std::vector<std::string>& b)
{
    if (a.size() != b.size())
        return false;
    for (size_t i = 0; i < a.size(); ++i)
        if (a[i] != b[i])
            return false;
    return true;
}

bool operator!=(const std::vector<std::string>& a, const std::vector<std::string>& b)
{
    return !(a == b);
}

bool operator==(const record& a, const record& b)
{
    return a.data == b.data;
}

bool operator!=(const record& a, const record& b)
{
    return !(a == b);
}


std::string line()
{
    std::string a;
    for (int i = 0; i < 20; ++i)
        a.push_back('-');
    a.push_back('\n');
    return a;
}

void wrong_arg()
{
    printf("Arguments error! A correct call should be: \n\n");
    printf("diff FILE FILE FILE [-CHN|-ENG]\n\n");
    printf("example: diff grade_old.txt grade_new.txt output.txt\n");
    printf("         diff old.dat new.dat out.dat -CHN\n");
    printf("    (by default the language is set to English)\n");
    exit(1);
}

double get_gpa(const std::vector<record>& a)
{
    double credit = 0, gp = 0;
    for (auto rec : a) {
        credit += stof(rec["xf"], 0);
        gp += stof(rec["jd"], 0) * stof(rec["xf"], 0);
    }
    if (credit == 0)
        return 0;
    return gp / credit;
}

std::vector<record> item_old, item_new;

char buff[MAX_BUFF_LEN];

void checkArgument(int argc, char const* argv[])
{
    if (argc < 4)
        wrong_arg();
    for (int i = 4; i < argc; ++i) {
        if (strcmp(argv[i], "-CHN") == 0)
            language = LANG_CHN;
        if (strcmp(argv[i], "-ENG") == 0)
            language = LANG_ENG;
        if (strcmp(argv[i], "-MARKDOWN") == 0)
            markdown = MARKDOWN;
        if (strcmp(argv[i], "-RAW") == 0)
            markdown = RAW;
    }
}

void getCategoryName()
{
    std::ifstream category_in("config/category.txt");
    while (category_in.getline(buff, MAX_BUFF_LEN)) {
        category.push_back(buff);
        low[category.back()] = category.size() - 1;
    }

    std::ifstream category_nam_in((language == LANG_CHN) ? "config/category_name_chn.txt" : "config/category_name_eng.txt");
    while (category_nam_in.getline(buff, MAX_BUFF_LEN))
        category_nam.push_back(buff);
}

void readOldData(const char* file)
{
    std::ifstream old_in(file);
    int n;
    old_in >> n;
    old_in.ignore();
    for (int i = 0; i < n; ++i) {
        record r;
        for (size_t j = 0; j < category.size(); ++j) {
            old_in.getline(buff, MAX_BUFF_LEN);
            r.data.push_back(buff);
        }
        item_old.push_back(r);
    }
}

void readNewData(const char* file)
{
    std::ifstream new_in(file);
    int m;
    new_in >> m;
    new_in.ignore();
    for (int i = 0; i < m; ++i) {
        record r;
        for (size_t j = 0; j < category.size(); ++j) {
            new_in.getline(buff, MAX_BUFF_LEN);
            r.data.push_back(buff);
        }
        item_new.push_back(r);
    }
}

void initAppeared()
{
    appeared_old.clear();
    appeared_old.resize(item_old.size());
    for (size_t i = 0; i < item_old.size(); ++i)
        appeared_old[i] = false;

    appeared_new.clear();
    appeared_new.resize(item_new.size());
    for (size_t i = 0; i < item_new.size(); ++i)
        appeared_new[i] = false;
}

void compareData()
{
    for (size_t i = 0; i < item_old.size(); ++i)
        for (size_t j = 0; j < item_new.size(); ++j) {
            if (appeared_new[j])
                continue;
            if (item_old[i]["kch"] == item_new[j]["kch"]) {
                appeared_old[i] = true;
                appeared_new[j] = true;
                if (item_old[i]["zzcj"] != item_new[j]["zzcj"])
                    changed.push_back(std::make_pair(i, j));
            }
        }

    for (size_t i = 0; i < item_new.size(); ++i)
        if (!appeared_new[i])
            newed.push_back(i);

    for (size_t i = 0; i < item_old.size(); ++i)
        if (!appeared_old[i])
            removed.push_back(i);
}

void writeLog(int argc, char const* argv[])
{
    printf("Comparing \"%s\" and \"%s\"\n", argv[1], argv[2]);
    printf("Output to \"%s\"\n", argv[3]);
    if (argc == 4)
        printf("No language parameter, default to ENG\n");
    else
        printf("Language parameter: %s\n", argv[4]);
    for (int i = 0; i < 20; ++i)
        printf("-");
    printf("\n");

    printf("CHANGE\n");
    for (auto a : changed) {
        printf("    Old #%d -> New #%d, kch: ", a.first, a.second);
        std::string s = item_old[a.first]["kch"];
        for (size_t i = 0; i < s.length(); ++i)
            printf("%c", s[i]);
        printf("\n");
    }
    if (changed.empty())
        printf("  none\n");

    printf("NEW\n");
    for (auto a : newed) {
        printf("  New #%d, kch: ", a);
        std::string s = item_new[a]["kch"];
        for (size_t i = 0; i < s.length(); ++i)
            printf("%c", s[i]);
        printf("\n");
    }
    if (newed.empty())
        printf("  none\n");

    printf("REMOVE\n");
    for (auto a : removed) {
        printf("  Old #%d, kch: ", a);
        std::string s = item_old[a]["kch"];
        for (size_t i = 0; i < s.length(); ++i)
            printf("%c", s[i]);
        printf("\n");
    }
    if (removed.empty())
        printf("  none\n");
}

void writeFile(const char* filename)
{
    int total = newed.size() + removed.size() + changed.size();

    std::ofstream output(filename);
    output << std::fixed << std::setprecision(3);
    if (total == 0)
        return;

    if (language == LANG_CHN) {
        output << "你的成绩有" << total << "处变动。\n";
        output << "均绩由" << get_gpa(item_old) << "变为" << get_gpa(item_new) << "。\n\n" << line();
    }
    else {
        output << "You have " << total << " grade updates.\n";
        output << "Your GPA changed from " << get_gpa(item_old) << " to " << get_gpa(item_new) << "\n\n" << line();
    }
    if (newed.size() != 0) {
        // output << newed.size() << " new grade are shown below:\n\n";
        for (size_t i = 0; i < newed.size(); ++i) {
            auto a = item_new[newed[i]];
            if (language == LANG_CHN)
                output << "[新成绩 #" << i + 1 << "]\n";
            else
                output << "[New grade #" << i + 1 << "]\n";
            output << a.fullform("kcmc");
            output << a.fullform("xf");
            output << a.fullform("zzcj");
            output << a.fullform("jd");
            output << std::endl;
        }
        output << line();
    }

    if (removed.size() != 0) {
        // output << removed.size() << " grade were removed. Which are:\n\n";
        for (size_t i = 0; i < removed.size(); ++i) {
            auto a = item_old[removed[i]];
            if (language == LANG_CHN)
                output << "[成绩取消 #" << i + 1 << "]\n";
            else
                output << "[Removed grade #" << i + 1 << "]\n";
            output << a.fullform("kcmc");
            output << a.fullform("xf");
            output << a.fullform("zzcj");
            output << a.fullform("jd");
            output << std::endl;
        }
        output << line();
    }

    if (changed.size() != 0) {
        // output << changed.size() << " grade were changed:\n\n";
        for (size_t i = 0; i < changed.size(); ++i) {
            auto a = item_old[changed[i].first];
            if (language == LANG_CHN)
                output << "[成绩变动 #" << i + 1 << "]\n";
            else
                output << "[Changed grade #" << i + 1 << "]\n";
            output << a.fullform("kcmc");
            output << a.fullform("xf");
            output << a.fullform("zzcj");
            output << a.fullform("jd");
            output << std::endl;
        }
    }
    if (language == LANG_CHN)
        output << "课程的详细信息请期待版本更新！\n";
    else
        output << "For detailed informations of courses, please wait for our new version.\n";
    output << "\nProudly powered by SgLy\n";
}

void writeMarkdown(const char* filename)
{
    int total = newed.size() + removed.size() + changed.size();

    std::ofstream output(filename);
    output << std::fixed << std::setprecision(3);
    if (total == 0)
        return;

    std::vector<int> category_to_print;
    category_to_print.push_back(low["kcmc"]);
    category_to_print.push_back(low["jsxm"]);
    category_to_print.push_back(low["xf"]);
    category_to_print.push_back(low["zzcj"]);
    category_to_print.push_back(low["jd"]);

    if (language == LANG_CHN) {
        output << "你的成绩有" << total << "处变动，";
        output << "均绩由" << get_gpa(item_old) << "变为" << get_gpa(item_new) << "。\n\n";
    }
    else {
        output << "You have " << total << " grade updates.\n";
        output << "Your GPA changed from " << get_gpa(item_old) << " to " << get_gpa(item_new) << "\n\n";
    }

    output << "| | ";
    for (auto a : category_to_print)
        output << category_nam[a] << " | ";
    output << "\n";

    output << "|---";
    for (size_t i = 0; i < category_to_print.size(); ++i)
        output << "|---";
    output << "|\n";

    if (newed.size() != 0) {
        for (size_t i = 0; i < newed.size(); ++i) {
            auto a = item_new[newed[i]];
            if (language == LANG_CHN)
                output << "| 新成绩 #" << i + 1 << " ";
            else
                output << "| New grade #" << i + 1 << " ";
            for (auto b : category_to_print)
                output << "| " << item_new[i].data[b] << " ";
            output << "|\n";
        }
        // output << line();
    }

    if (removed.size() != 0) {
        // output << removed.size() << " grade were removed. Which are:\n\n";
        for (size_t i = 0; i < removed.size(); ++i) {
            auto a = item_old[removed[i]];
            if (language == LANG_CHN)
                output << "| 成绩取消 #" << i + 1 << " ";
            else
                output << "| Removed grade #" << i + 1 << " ";
            for (auto b : category_to_print)
                output << "| " << item_old[i].data[b] << " ";
            output << "|\n";
        }
        output << line();
    }

    if (changed.size() != 0) {
        // output << changed.size() << " grade were changed:\n\n";
        for (size_t i = 0; i < changed.size(); ++i) {
            auto a = item_old[changed[i].first];
            auto b = item_new[changed[i].second];
            if (language == LANG_CHN)
                output << "| 成绩变动 #" << i + 1 << " ";
            else
                output << "| Changed grade #" << i + 1 << " ";
            for (auto c : category_to_print)
                if (a.data[c] == b.data[c])
                    output << "| " << a.data[c] << " ";
                else {
                    output << "| " << a.data[c] << " -> ";
                    output << b.data[c] << " ";
                }
            output << "|\n";
        }
    }

    output << "\n";
    if (language == LANG_CHN)
        output << "课程的详细信息请期待版本更新！\n";
    else
        output << "For detailed informations of courses, please wait for our new version.\n";
    output << "\nProudly powered by SgLy\n";
}

int main(int argc, char const* argv[])
{
    checkArgument(argc, argv);
    getCategoryName();
    readOldData(argv[1]);
    readNewData(argv[2]);
    initAppeared();
    compareData();
    writeLog(argc, argv);
    if (markdown == MARKDOWN)
        writeMarkdown(argv[3]);
    else
        writeFile(argv[3]);
    return 0;
}
