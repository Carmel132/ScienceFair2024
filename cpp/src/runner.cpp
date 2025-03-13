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
// Next Step
void Runner::back() {
  if (phaseIdx <= 0) {
    std::cerr << "Cannot move backward!\n";
    return;
  }
  phaseIdx--;
  actions.at(phaseIdx)->reverse(maze);
}
// Next Step
void Runner::next() {
  std::cout << "in next: " << actions.size() << '\n';
  if (phaseIdx >= actions.size()) {
    std::cerr << "Cannot move forward!\n";
    return;
  }
  actions.at(phaseIdx)->run(maze);
  phaseIdx++;
}

// TODO: Refactor [Runner::parseLines] into more functions
void Runner::parseLines(std::vector<std::string> lines) {
  actions = std::vector<std::unique_ptr<ActionPhase>>();
  ActionPhase *actionPhase;
  ActionStep *actionStep = new ActionStep();
  for (int i = Runner::metadataLines; i < lines.size(); ++i) {
    // "---" indicates end of [ActionStep]
    if (lines[i].compare("---") == 0) {
      actionPhase->add(std::unique_ptr<ActionStep>(actionStep));
      actionStep = new ActionStep();
      continue;
    }
    std::smatch matches;

    // ">>>" indicates end of [ActionPhase]/*
    if (std::regex_search(lines[i], matches, ActionPhase::pattern)) {
      if (!actionPhase)
        actions.push_back(std::unique_ptr<ActionPhase>(actionPhase));
      actionPhase = new ActionPhase(matches[1]);
      continue;
    }
    if (std::regex_search(lines[i], matches, Runner::parseLineRegex)) {
      if (matches[1].compare("SETCELL") == 0) {
        actionStep->add(std::make_unique<SetCell>(lines[i]));
      }
    } else {
      std::cerr << "(57) Could not identify action: " << lines[i] << "\n";
    }
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
  if (std::regex_search(meta_mazeSize, matches, metaMazeSize)) {
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
}

void SetCell::reverse(std::shared_ptr<MazeState> maze) {
  maze->set(loc.first, loc.second, old);
}

void SetCell::run(std::shared_ptr<MazeState> maze) {
  maze->set(loc.first, loc.second, _new);
}

SetCell::SetCell(std::string log) {
  std::smatch matches;
  if (std::regex_search(log, matches, pattern)) {
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
  for (auto action : actions) {
    action->reverse(maze);
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
  for (auto action : actions) {
    action->reverse(maze);
  }
}
