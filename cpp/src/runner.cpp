#include "runner.h"

Runner::Runner(std::shared_ptr<MazeState>* out) {
    std::ifstream file("../../out.txt");
    if (!file.is_open()) {
        std::cerr << "Could not open file!\n";
        throw std::runtime_error("Could not open file: ");
    }
    std::ostringstream oss;
    oss << file.rdbuf();
    Runner(oss.str(), out);
}

void Runner::back() {
    if (idx <= actions.size()) {
        std::cerr << "Cannot move backward!\n";
        return;
    }
    idx--;
    actions[idx]->reverse(maze);
}

void Runner::next() {
    if (idx >= actions.size()) {
        std::cerr << "Cannot move forward!\n";
        return;
    }
    idx++;
    actions[idx]->run(maze);
}

void Runner::parseLines(std::vector<std::string> lines) {
    for (int i = metadataLines + 1; i < lines.size(); ++i) {
        std::smatch matches;
        if (std::regex_search(lines[i], matches, parseLineRegex)) {

            if (matches[1].compare("SETCELL")) {
                actions.push_back(new SetCell(lines[i]));
            }
        }

    }
}

Runner::Runner(std::string log, std::shared_ptr<MazeState>* out) {
    std::istringstream stream(log);
    std::string line;
    std::vector<std::string> lines;

    while(std::getline(stream, line)){
        lines.push_back(line);
    }

    std::smatch matches;
    std::string meta_mazeSize = lines[0];
    if (std::regex_search(meta_mazeSize, matches, metaMazeSize)) {
        try {
            maze =std::make_shared<MazeState>(std::stoi(matches[1].str()), std::stoi(matches[2].str()));
        }
        catch (std::exception e) {
            maze = std::make_shared<MazeState>(5, 5);
            std::cerr << "Error: " << e.what();
        }

    }
    else {
        std::cerr << "Error: Couldn't instatiate Runner object: Failed to parse Maze Size metadata\n";
    }

    idx = 0;
    if (out) {
        *out = maze;
    }

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
        loc = std::pair<int, int>(std::stoi(matches[1].str()), std::stoi(matches[2].str()));
        old = std::stoi(matches[3].str());
        _new = std::stoi(matches[4].str());
    }
    else {
        std::cerr << "Error: Unable to read input. Given string: " << log << "\n";
    }
}