#pragma once
#include <regex>
#include <state.h>
#include <string>
#include <utility>
#include <fstream>
#include <sstream>
#include <memory>
class ActionPattern {
public:
    const std::regex pattern;


    virtual void run(std::shared_ptr<MazeState> maze) =0;
    virtual void reverse(std::shared_ptr<MazeState> maze)=0;
};

class SetCell : public ActionPattern {
public:
    const std::regex pattern{R"(loc=\(([0-9]+), ([0-9]+)\), old=([0-9]+), new=([0-9]+))"};
    std::pair<int,int> loc;
    int old, _new;
    void run(std::shared_ptr<MazeState> maze);
    void reverse(std::shared_ptr<MazeState> maze);
    SetCell(std::string log);
};

class Runner {
public:
    Runner(std::shared_ptr<MazeState>* out);
    Runner(std::string log, std::shared_ptr<MazeState>* out);

    void next();
    void back();

private:
    void parseLines(std::vector<std::string> lines);
    const std::regex parseLineRegex{R"(TYPE=(\w+))"};

    const std::regex metaMazeSize{R"(DIM: \(([0-9]+), ([0-9]+))"};

    std::shared_ptr<MazeState> maze;
    std::vector<ActionPattern*> actions;
    int idx;
    const int metadataLines = 1;
};