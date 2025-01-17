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
    MazeState();

    std::string toString() const;

    int get(int x, int y) const;
    void set(int x, int y, int val);

    int getWidth() {return width;}
    int getHeight() {return height;}
private:

    int width;
    int height;
    std::vector<std::vector<int>> cells;
};
