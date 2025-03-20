#pragma once
#include <fstream>
#include <memory>
#include <regex>
#include <sstream>
#include <state.h>
#include <string>
#include <utility>
class ActionPattern {
public:
  virtual void run(std::shared_ptr<MazeState> maze) = 0;
  virtual void reverse(std::shared_ptr<MazeState> maze) = 0;
  virtual ~ActionPattern() = default;
};

class SetCell : public ActionPattern {
public:
  static const std::regex &getPattern() {
    const static std::regex pattern{
        R"(loc=\(([0-9]+), ([0-9]+)\), old=([0-9]+), new=([0-9]+))"};
    return pattern;
  }

  std::pair<int, int> loc;
  int old, _new;
  void run(std::shared_ptr<MazeState> maze);
  void reverse(std::shared_ptr<MazeState> maze);
  SetCell(std::string log);
};

class GetCell : public ActionPattern {
public:
  static const std::regex &getPattern() {
    const static std::regex pattern{
        R"(loc=\(([0-9]+), ([0-9]+)\), val=([0-9]+))"};
    return pattern;
  }

  std::pair<int, int> loc;
  int val;
  void run(std::shared_ptr<MazeState> maze);
  void reverse(std::shared_ptr<MazeState> maze);
  GetCell(std::string log);
};

class ActionStep : public ActionPattern {
public:
  void add(std::shared_ptr<ActionPattern> pattern);
  void run(std::shared_ptr<MazeState> maze);
  void reverse(std::shared_ptr<MazeState> maze);

private:
  std::vector<std::shared_ptr<ActionPattern>> actions;
};
// TODO: Add comments to explain what EVERYTHING does
class ActionPhase : public ActionPattern {
public:
  static const std::regex &getPattern() {
    static const std::regex pattern{R"((>>>) (\w+))",
                                    std::regex_constants::ECMAScript};
    return pattern;
  }
  void add(std::shared_ptr<ActionStep> pattern);
  void run(std::shared_ptr<MazeState> maze);
  void reverse(std::shared_ptr<MazeState> maze);
  std::shared_ptr<ActionStep> get(int idx) const;
  inline int getSize() const { return actions.size(); }

  ActionPhase(std::string _name) : name{_name} {}

private:
  std::vector<std::shared_ptr<ActionStep>> actions;
  std::string name;
};

struct ActionPhaseRunner {
public:
  // Moves the runner to the next ActionStep. Returns whether the Runner is at
  // the end bound
  bool next() {
    bool atFrontBound = idx >= actionSize - 1;
    idx = std::min(idx + 1, actionSize - 1);
    return atFrontBound;
  }

  // Moves the runner to the previous ActionStep. Returns whether the Runner is
  // at the start bound
  bool back() {
    bool atBackBound = idx == 0;
    idx = std::max(idx - 1, 0);
    return atBackBound;
  }
  std::shared_ptr<ActionStep> get() const { return actions->get(idx); }
  ActionPhaseRunner(const std::shared_ptr<ActionPhase> &_actions)
      : actions{_actions}, idx{0}, actionSize{_actions->getSize()} {};

private:
  int idx;
  int actionSize;
  std::shared_ptr<ActionPhase> actions;
};

// Parses output file and provides running functionality on the provided
// [MazeState]
class Runner {
public:
  Runner(std::shared_ptr<MazeState> &out);
  Runner(std::string log, std::shared_ptr<MazeState> &out);
  Runner(std::string log);

  void next();
  void back();

  void nextPhase();
  void previousPhase();

  void end();
  void start();

private:
  void parseLines(std::vector<std::string> lines);
  static const std::regex &getParseLinePattern() {
    const static std::regex pattern{R"(TYPE=(\w+))"};
    return pattern;
  }

  static const std::regex &getMetaMazeSizePattern() {
    const static std::regex pattern{R"(DIM: \(([0-9]+), ([0-9]+))"};
    return pattern;
  }
  std::shared_ptr<MazeState> maze;
  std::vector<ActionPhaseRunner> actions;
  int phaseIdx;
  const int metadataLines = 1;
};
