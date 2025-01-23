#include "render.h"
void OutlineColoredRect::render(SDL_Renderer* renderer) {
    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);
    SDL_Rect r = toSDL_Rect();
    SDL_RenderDrawRect(renderer, &r);
}

void ColoredRect::render(SDL_Renderer* renderer) {
    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);
    SDL_Rect r = toSDL_Rect();
    SDL_RenderFillRect(renderer, &r);
}

ColoredRect::ColoredRect(int _x, int _y, int _w, int _h, const Color& _color) : Rect(_x, _y, _w, _h) {
    color=_color;
}

void Rect::render(SDL_Renderer* renderer) {
    SDL_Rect r = toSDL_Rect();
    SDL_RenderFillRect(renderer, &r);
}

SDL_Rect Rect::toSDL_Rect() const {
    return {x,y,w,h};
}

Rect::Rect(int _x, int _y, int _w, int _h){
    x=_x;
    y=_y;
    w=_w;
    h=_h;
}

Rect::Rect(const Point& p1, const Point& p2){
    x = std::min(p1.x, p2.x);
    y = std::min(p1.y, p2.y);
    w = std::abs(p1.x-p2.x);
    h = std::abs(p1.y-p2.y);
}

void GameRenderer::GenerateCellPoints(ScreenDimensions& screenDimensions) {
        int dx = std::min((screenDimensions.pxHeight-screenDimensions.padding) / screenDimensions.cellHeight, (screenDimensions.pxWidth - screenDimensions.padding) / screenDimensions.cellWidth);
        Point centerOffset = Point((screenDimensions.pxWidth - screenDimensions.cellWidth * dx) / 2, (screenDimensions.pxHeight - screenDimensions.cellHeight * dx) / 2);
        std::cout << "dx: " << dx << ", cox: " << centerOffset.x << ", coy: " << centerOffset.y << "\n";
        for (int x = 0; x < screenDimensions.cellWidth; ++x) {
            std::vector<Point> v;
            for (int y = 0; y < screenDimensions.cellHeight; ++y) {
                v.push_back(Point(centerOffset.x + x * dx, centerOffset.y + y * dx));
            }
            cellPoints.push_back(v);
        }
        screenDimensions.cellSize = dx;
}

int GameRenderer::initSDL() {
    int Success = 1;

    if(SDL_Init(SDL_INIT_VIDEO) != 0)
    {
        SDL_Log("Failed to initialize SDL! SDL_GetError: %s\n", SDL_GetError());
        Success = 0;
    }
    else
    {
        window = SDL_CreateWindow("SDL Test",
                                  SDL_WINDOWPOS_UNDEFINED,
                                  SDL_WINDOWPOS_UNDEFINED,
                                  640,
                                  480,
                                  0);
        if(!window)
        {
            SDL_Log("Failed to create window! SDL_GetError: %s\n", SDL_GetError());
            Success = 0;
        }
        else
        {
            renderer= SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
            if(!renderer)
            {
                SDL_Log("Failed to create renderer!\n");
                Success = 0;
            }
            else
            {
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
    window =  NULL;

    SDL_Quit();

}

void GameRenderer::clear() {
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0xff);
    SDL_RenderClear(renderer);
}


void GameRenderer::present() {
    SDL_RenderPresent(renderer);
}

void GameRenderer::GenerateCellRects(const MazeState& maze, const ScreenDimensions& dim) {
    cellRects.objs.clear();
    for (int i = 0; i < cellPoints.size(); ++i) {
        for (int j = 0; j < cellPoints[i].size(); ++j) {
            if (maze.get(i, j)) {
                Rect rect = Rect(cellPoints[i][j].x, cellPoints[i][j].y, dim.cellSize, dim.cellSize);
                cellRects.objs.push_back(rect);
            }
        }
    }
}

void GameRenderer::renderCells() {
    SDL_SetRenderDrawColor(renderer, 0xFF, 0xFF, 0xFF, 0xff);
    cellRects.render(renderer);
}

void GameRenderer::render() {
    clear();

    renderCells();

    present();
}
