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
    virtual void run(std::shared_ptr<MazeState> maze) =0;
    virtual void reverse(std::shared_ptr<MazeState> maze)=0;
    virtual ~ActionPattern() = default;

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

class ActionStep : public ActionPattern {
public:
    void add(std::shared_ptr<ActionPattern> pattern);
    void run(std::shared_ptr<MazeState> maze);
    void reverse(std::shared_ptr<MazeState> maze);
private:
    std::vector<std::shared_ptr<ActionPattern>> actions;
};

// Parses output file and provides running functionality on the provided [MazeState]
class Runner {
public:
    Runner(std::shared_ptr<MazeState>& out);
    Runner(std::string log, std::shared_ptr<MazeState>& out);
    Runner(std::string log);

    void next();
    void back();

    void end();
    void start();

private:
    void parseLines(std::vector<std::string> lines);
    const std::regex parseLineRegex{R"(TYPE=(\w+))"};

    const std::regex metaMazeSize{R"(DIM: \(([0-9]+), ([0-9]+))"};

    std::shared_ptr<MazeState> maze;
    std::vector<std::unique_ptr<ActionStep>> actions;
    int idx;
    const int metadataLines =1;
};
