#include "runner.h"
#include <memory>

void Runner::end() {
  while (phaseIdx < actions.size()) {
    next();
  }
}

void Runner::start() {
  while (phaseIdx > 0) {
    back();
  }
}

Runner::Runner(std::shared_ptr<MazeState> &out)
    : Runner(
          [&]() -> std::string {
            std::ifstream file(
                "C:/Users/User/vclib/C++/ScienceFair2024/out.txt");
            if (!file.is_open()) {
              std::cerr << "Could not open file!\n";

              throw std::runtime_error("Could not open file: ");
            }
            std::ostringstream oss;
            oss << file.rdbuf();
            return oss.str();
          }(),
          out) {}

// TODO: Fix bug where you have to click twice when changing from moving forward
// to backward and vice versa

// Next Step
void Runner::back() {
  ActionPhaseRunner &actionPhaseRunner = actions.at(phaseIdx);
  actionPhaseRunner.get()->reverse(maze);
  bool atBackBound = actionPhaseRunner.back();
  if (atBackBound) {
    if (phaseIdx <= 0) {
      std::cerr << "Cannot move phase backward!\n";
      return;
    }
    phaseIdx--;
    return;
  }
}
// Next Step
void Runner::next() {
  std::cout << "Phase Idx: " << phaseIdx << "\n";
  ActionPhaseRunner &actionPhaseRunner = actions.at(phaseIdx);

  actionPhaseRunner.get()->run(maze);
  bool atFrontBound = actionPhaseRunner.next();
  if (atFrontBound) {
    if (phaseIdx >= actions.size() - 1) {
      std::cerr << "Cannot move forward!\n";
      return;
    }
    phaseIdx++;
    return;
  }
}

// TODO: Refactor [Runner::parseLines] into more functions
void Runner::parseLines(std::vector<std::string> lines) {
  actions = std::vector<ActionPhaseRunner>();
  ActionPhase *actionPhase = 0;
  ActionStep *actionStep = new ActionStep();
  for (int i = Runner::metadataLines; i < lines.size(); ++i) {
    std::string __s = lines[i];

    // "---" indicates end of [ActionStep]
    if (lines[i].compare("---") == 0) {
      actionPhase->add(std::unique_ptr<ActionStep>(actionStep));
      actionStep = new ActionStep();
      continue;
    }
    std::smatch matches;

    // ">>>" indicates start of [ActionPhase]/*
    if (std::regex_search(lines[i], matches, ActionPhase::getPattern())) {
      if (actionPhase) {
        actions.push_back(
            ActionPhaseRunner(std::unique_ptr<ActionPhase>(actionPhase)));
      }
      actionPhase = new ActionPhase(matches[1]);
      continue;
    }
    if (std::regex_search(lines[i], matches, Runner::getParseLinePattern())) {
      if (matches[1].compare("SETCELL") == 0) {
        actionStep->add(std::make_unique<SetCell>(lines[i]));
      }
    } else {
      std::cerr << "(57) Could not identify action: " << lines[i] << "\n";
    }
  }
  if (actionPhase) {
    actions.push_back(
        ActionPhaseRunner(std::unique_ptr<ActionPhase>(actionPhase)));
  }
}

Runner::Runner(std::string log, std::shared_ptr<MazeState> &out) : Runner(log) {
  std::cout << "Called new constructor";
  out = maze;
}

Runner::Runner(std::string log) {
  std::istringstream stream(log);
  std::string line;
  std::vector<std::string> lines;
  std::cout << "reached constructor";
  while (std::getline(stream, line)) {
    lines.push_back(line);
  }

  std::smatch matches;
  std::string meta_mazeSize = lines[0];
  if (std::regex_search(meta_mazeSize, matches, getMetaMazeSizePattern())) {
    try {
      std::cout << "got to make maze";
      maze = std::make_shared<MazeState>(std::stoi(matches[1].str()),
                                         std::stoi(matches[2].str()));
    } catch (const std::exception &e) {
      maze = std::make_shared<MazeState>(5, 5);
      std::cerr << "Error: " << e.what() << "\n";
    }

  } else {
    std::cerr << "(86) Couldn't instatiate Runner object: Failed to parse Maze "
                 "Size metadata\n";
  }

  phaseIdx = 0;

  parseLines(lines);
  std::cout << actions.size();
}

void SetCell::reverse(std::shared_ptr<MazeState> maze) {
  maze->set(loc.first, loc.second, old);
}

void SetCell::run(std::shared_ptr<MazeState> maze) {
  maze->set(loc.first, loc.second, _new);
}

SetCell::SetCell(std::string log) {
  std::smatch matches;
  if (std::regex_search(log, matches, SetCell::getPattern())) {
    loc = std::pair<int, int>(std::stoi(matches[1].str()),
                              std::stoi(matches[2].str()));
    old = std::stoi(matches[3].str());
    _new = std::stoi(matches[4].str());
  } else {
    std::cerr << "(112) Unable to read input. Given string: " << log << "\n";
  }
}

void ActionStep::add(std::shared_ptr<ActionPattern> action) {
  actions.push_back(action);
}

void ActionStep::run(std::shared_ptr<MazeState> maze) {
  for (auto action : actions) {
    action->run(maze);
  }
}

void ActionStep::reverse(std::shared_ptr<MazeState> maze) {
  for (int i = actions.size() - 1; i >= 0; --i) {
    actions.at(i)->reverse(maze);
  }
}

void ActionPhase::add(std::shared_ptr<ActionStep> pattern) {
  actions.push_back(pattern);
}

void ActionPhase::run(std::shared_ptr<MazeState> maze) {
  for (auto action : actions) {
    action->run(maze);
  }
}

void ActionPhase::reverse(std::shared_ptr<MazeState> maze) {
  for (size_t i = actions.size() - 1; i >= 0; --i) {
    actions.at(i)->reverse(maze);
  }
}

std::shared_ptr<ActionStep> ActionPhase::get(int idx) const {
  return actions.at(idx);
}
