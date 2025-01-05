#pragma once
#include <regex>
#include <state.h>
#include <string>
#include <utility>
class ActionPattern {
public:
    std::regex pattern;
    std::string type;

    MazeState run(MazeState& maze);
    MazeState reverse(MazeState& maze);
};

class SetCell : ActionPattern {
public:
    std::regex pattern{R"(loc=\(([0-9]+), ([0-9]+)\), old=([0-9]+), new=([0-9]+), TYPE=[A-Za-z\.]+)"};
    std::pair<int,int> loc;
    int old, _new;
    MazeState run(MazeState& maze);
    MazeState reverse(MazeState& maze);
    SetCell(std::string log);
};