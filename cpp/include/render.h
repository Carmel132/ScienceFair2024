#pragma once
#include "runner.h"
#include "state.h"
#ifdef __linux__
#include "SDL2/SDL.h"
#else
#include "SDL.h"
#endif
#include "algorithm"
#include "vector"
struct Point {
  int x, y;
  Point(int _x, int _y) : x{_x}, y{_y} {};
};

struct Color {
  int r, g, b, a;

  Color() : Color(0, 0, 0) {};
  Color(int _r, int _g, int _b, int _a = 0xFF) : r{_r}, g{_g}, b{_b}, a{_a} {};
};

struct ScreenDimensions {
  int pxWidth, pxHeight, cellWidth, cellHeight;
  int cellSize;
  int padding; // Pixel buffer between edge of screen and maze
};

class Renderable {
public:
  virtual void render(SDL_Renderer *renderer) = 0;
  virtual ~Renderable() = default;
};

class Rect : public Renderable {
public:
  int x, y, w, h;

  Rect(int _x, int _y, int _w, int _h);
  Rect(const Point &p1, const Point &p2);

  SDL_Rect toSDL_Rect() const;

  void render(SDL_Renderer *renderer); // Renders a filled rect;
};

class ColoredRect : public Rect {
public:
  Color color;
  ColoredRect(int _x, int _y, int _w, int _h, const Color &_color);

  void render(SDL_Renderer *renderer);
};

class OutlineColoredRect : public ColoredRect {
public:
  void render(SDL_Renderer *renderer);
  OutlineColoredRect(int _x, int _y, int _w, int _h, const Color &_color)
      : ColoredRect(_x, _y, _w, _h, _color) {};
};

template <class RenderableType> class RenderableGroup : public Renderable {
  static_assert(std::is_base_of<Renderable, RenderableType>(),
                "T must inherit from Renderable");

public:
  std::vector<RenderableType> objs;

  RenderableGroup() : objs{} {};

  void render(SDL_Renderer *renderer) override {
    for (RenderableType obj : objs) {
      obj.render(renderer);
    }
  }
};

struct GameRendererData {

  std::vector<std::vector<Point>> cellPoints;
  RenderableGroup<Rect> cellRects;

  GameRendererData() : cellPoints{}, cellRects{} {}
};

struct GameRenderer {

  SDL_Window *window;
  SDL_Renderer *renderer;
  GameRendererData data;
  void render();

  void GenerateCellPoints(ScreenDimensions &screenDimensions);
  void GenerateCellRects(const MazeState &maze, const ScreenDimensions &dim);
  void renderCells();

  GameRenderer() : data{} {}

  void clear();
  void present();

  int initSDL();
  void shutDownSDL();

private:
  bool hasAdjacentInMaze(const Point &point, const MazeState &maze,
                         int val) const;
};

void RenderCells(SDL_Renderer *renderer,
                 const std::vector<std::vector<Point>> &points,
                 const MazeState &maze, const ScreenDimensions &dim);

// General structure to render an [ActionPattern]. Object will not render
// unless you define a custom implementation of a given [ActionPattern] subclass
template <class T> class RenderActionPattern : public Renderable {
  static_assert(std::is_base_of<ActionPattern, T>(),
                "T must inherit from ActionPattern");

public:
  void render(SDL_Renderer *renderer) override {}

  RenderActionPattern(const T &_action, const MazeState &_maze,
                      const ScreenDimensions &_dim,
                      const GameRendererData &_data)
      : action{_action}, maze{_maze}, dim{_dim}, data{_data} {};

protected:
  T action;
  const MazeState &maze;
  const ScreenDimensions &dim;
  const GameRendererData &data;
};
