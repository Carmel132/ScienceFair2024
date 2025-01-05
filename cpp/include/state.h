#pragma once
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
#include <iterator>
#include <iostream>
class MazeState {
public:
    MazeState(int _width, int _height);
    
    std::string toString() const;

    int get(int x, int y) const;
    void set(int x, int y, int val);
private:

    int width;
    int height;
    std::vector<std::vector<int>> cells;
};