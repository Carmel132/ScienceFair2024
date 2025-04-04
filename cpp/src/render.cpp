#include "render.h"
void OutlineColoredRect::render(SDL_Renderer *renderer) {
  SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);
  SDL_Rect r = toSDL_Rect();
  SDL_RenderDrawRect(renderer, &r);
}

void ColoredRect::render(SDL_Renderer *renderer) {
  SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);
  SDL_Rect r = toSDL_Rect();
  SDL_RenderFillRect(renderer, &r);
}

ColoredRect::ColoredRect(int _x, int _y, int _w, int _h, const Color &_color)
    : Rect(_x, _y, _w, _h) {
  color = _color;
}

void Rect::render(SDL_Renderer *renderer) {
  SDL_Rect r = toSDL_Rect();
  SDL_RenderFillRect(renderer, &r);
}

SDL_Rect Rect::toSDL_Rect() const { return {x, y, w, h}; }

Rect::Rect(int _x, int _y, int _w, int _h) {
  x = _x;
  y = _y;
  w = _w;
  h = _h;
}

Rect::Rect(const Point &p1, const Point &p2) {
  x = std::min(p1.x, p2.x);
  y = std::min(p1.y, p2.y);
  w = std::abs(p1.x - p2.x);
  h = std::abs(p1.y - p2.y);
}

void GameRenderer::GenerateCellPoints(ScreenDimensions &screenDimensions) {
  int dx = std::min((screenDimensions.pxHeight - screenDimensions.padding) /
                        screenDimensions.cellHeight,
                    (screenDimensions.pxWidth - screenDimensions.padding) /
                        screenDimensions.cellWidth);
  Point centerOffset =
      Point((screenDimensions.pxWidth - screenDimensions.cellWidth * dx) / 2,
            (screenDimensions.pxHeight - screenDimensions.cellHeight * dx) / 2);
  std::cout << "dx: " << dx << ", cox: " << centerOffset.x
            << ", coy: " << centerOffset.y << "\n";
  for (int x = 0; x < screenDimensions.cellWidth; ++x) {
    std::vector<Point> v;
    for (int y = 0; y < screenDimensions.cellHeight; ++y) {
      v.push_back(Point(centerOffset.x + x * dx, centerOffset.y + y * dx));
    }
    data.cellPoints.push_back(v);
  }
  screenDimensions.cellSize = dx;
  std::cout << "Generated "
            << data.cellPoints.size() * data.cellPoints.at(0).size()
            << " points\n";
}

int GameRenderer::initSDL() {
  int Success = 1;

  if (SDL_Init(SDL_INIT_VIDEO) != 0) {
    SDL_Log("Failed to initialize SDL! SDL_GetError: %s\n", SDL_GetError());
    Success = 0;
  } else {
    window = SDL_CreateWindow("SDL Test", SDL_WINDOWPOS_UNDEFINED,
                              SDL_WINDOWPOS_UNDEFINED, 640, 480, 0);
    if (!window) {
      SDL_Log("Failed to create window! SDL_GetError: %s\n", SDL_GetError());
      Success = 0;
    } else {
      renderer = SDL_CreateRenderer(
          window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
      if (!renderer) {
        SDL_Log("Failed to create renderer!\n");
        Success = 0;
      } else {
        SDL_SetRenderDrawColor(renderer, 0xff, 0xff, 0xff, 0xff);
      }
    }
  }

  return Success;
}

void GameRenderer::shutDownSDL() {
  SDL_DestroyRenderer(renderer);
  SDL_DestroyWindow(window);
  renderer = NULL;
  window = NULL;

  SDL_Quit();
}

void GameRenderer::clear() {
  SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0xff);
  SDL_RenderClear(renderer);
}

void GameRenderer::present() { SDL_RenderPresent(renderer); }

// Generates the rects of the white cells
void GameRenderer::GenerateCellRects(const MazeState &maze,
                                     const ScreenDimensions &dim) {
  data.cellRects.objs.clear();
  for (int i = 0; i < data.cellPoints.size(); ++i) {
    for (int j = 0; j < data.cellPoints[i].size(); ++j) {
      bool pathAroundOddEntry =
          (i % 2 && j % 2) &&
          !hasAdjacentInMaze(Point(i, j), maze,
                             0); // Makes it so path moves by 3 every time
      if (maze.get(i, j) || pathAroundOddEntry) {

        Rect rect = Rect(data.cellPoints[i][j].x, data.cellPoints[i][j].y,
                         dim.cellSize, dim.cellSize);
        data.cellRects.objs.push_back(rect);
      }
    }
  }
}

// Renders white wall cells
void GameRenderer::renderCells() {
  SDL_SetRenderDrawColor(renderer, 0xFF, 0xFF, 0xFF, 0xff);
  data.cellRects.render(renderer);
}

void GameRenderer::render() {
  clear();

  renderCells();

  present();
}

// Checks whether adjacent points (horizontally and vetically) in the maze
// relative to [point] contain [val]
bool GameRenderer::hasAdjacentInMaze(const Point &point, const MazeState &maze,
                                     int val) const {
  static const Point dirs[4] = {Point(1, 0), Point(0, 1), Point(-1, 0),
                                Point(0, -1)};
  for (Point p : dirs) {
    int x = point.x + p.x;
    int y = point.y + p.y;
    if (maze.get(point.x + p.x, point.y + p.y) == val) {
      return true;
    }
  }
  return false;
}

template <> void RenderActionPattern<GetCell>::render(SDL_Renderer *renderer) {
  Point point{data.cellPoints.at(action.loc.first).at(action.loc.second)};
  const static Color drawColor{255, 0, 0};
  ColoredRect drawRect{point.x, point.y, dim.cellSize, dim.cellSize, drawColor};
  drawRect.render(renderer);
}
