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
  const std::regex pattern{
      R"(loc=\(([0-9]+), ([0-9]+)\), old=([0-9]+), new=([0-9]+))"};
  std::pair<int, int> loc;
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
// TODO: Add comments to explain what EVERYTHING does
class ActionPhase : public ActionPattern {
public:
  inline static const std::regex pattern{R"(>>>) (\w+)"};
  void add(std::shared_ptr<ActionStep> pattern);
  void run(std::shared_ptr<MazeState> maze);
  void reverse(std::shared_ptr<MazeState> maze);

  inline int getSize() const { return actions.size(); }

  ActionPhase(std::string _name) : name{_name} {}

private:
  std::vector<std::shared_ptr<ActionStep>> actions;
  std::string name;
};
// TODO: to complete this runner, add a get method to the [ActionPhase] class
struct ActionPhaseRunner {
public:
  // Moves the runner to the next ActionStep. Returns whether the Runner is at
  // the end bound
  bool next() {
    idx = std::min(idx + 1, actionSize - 1);
    return idx >= actionSize;
  }

  // Moves the runner to the previous ActionStep. Returns whether the Runner is
  // at the start bound
  bool back() {
    idx = std::max(idx - 1, 0);
    return idx < 0;
  }

  ActionPhaseRunner(const ActionPhase &_actions)
      : actions{_actions}, idx{0}, actionSize{_actions.getSize()} {};

private:
  int idx;
  int actionSize;
  ActionPhase actions;
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

  void end();
  void start();

private:
  void parseLines(std::vector<std::string> lines);
  inline const static std::regex parseLineRegex{R"(TYPE=(\w+))"};

  inline const static std::regex metaMazeSize{R"(DIM: \(([0-9]+), ([0-9]+))"};

  std::shared_ptr<MazeState> maze;
  std::vector<std::unique_ptr<ActionPhase>> actions;
  int phaseIdx, stepIdx;
  const int metadataLines = 1;
};
