#include "runner.h"

SetCell::SetCell(std::string log) {
    std::smatch matches;
    std::cerr << "pattern: " << "loc=\(([0-9]+), ([0-9]+)\), old=([0-9]+), new=([0-9]+)" << "\n";
    if (std::regex_search(log, matches, pattern)) {
        loc = std::pair<int, int>(std::stoi(matches[1].str()), std::stoi(matches[2].str()));
        old = std::stoi(matches[3].str());
        _new = std::stoi(matches[4].str());
    }
    else {
        std::cerr << "Error: Unable to read input. Given string: " << log << "\n";
    }
}