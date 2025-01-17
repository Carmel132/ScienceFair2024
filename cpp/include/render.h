#pragma once
#include "state.h"
#ifdef __linux__
#include "SDL2/SDL.h"
#else
#include "SDL.h"
#endif
#include "algorithm"
#include "vector"
struct Point {
    int x,y;
    Point(int _x, int _y) : x{_x}, y{_y} {};
};

struct Color {
    int r,g,b,a;


    Color(): Color(0,0,0){};
    Color(int _r, int _g, int _b, int _a=0xFF): r{_r}, g{_g}, b{_b}, a{_a} {};
};

struct ScreenDimensions {
    int pxWidth, pxHeight, cellWidth, cellHeight;
    int cellSize;
    int padding; // Pixel buffer between edge of screen and maze
};

class Renderable
{
    public:
    virtual void render(SDL_Renderer* renderer) = 0;
    virtual ~Renderable() = default;
};

class Rect : public Renderable{
public:

    int x,y,w,h;


    Rect(int _x,int _y,int _w, int _h);
    Rect(const Point& p1, const Point& p2);

    SDL_Rect toSDL_Rect() const;

    void render(SDL_Renderer* renderer); // Renders a filled rect;

};

class ColoredRect : public Rect {
public:
    Color color;
    ColoredRect(int _x, int _y, int _w, int _h, const Color& _color);

    void render(SDL_Renderer* renderer);
};

class OutlineColoredRect : public ColoredRect {
    public:
    void render(SDL_Renderer* renderer);
    OutlineColoredRect(int _x, int _y, int _w, int _h, const Color& _color) : ColoredRect(_x,_y,_w,_h,_color) {};
};

void RenderCells(SDL_Renderer* renderer, const std::vector<std::vector<Point>>& points, const MazeState& maze, const ScreenDimensions& dim);
