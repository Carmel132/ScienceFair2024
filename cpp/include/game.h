#pragma once
#ifdef __linux__
#include "SDL2/SDL.h"
#else
#include "SDL.h"
#endif

#include "render.h"
#include <iostream>
#include <vector>
#include "runner.h"
class Game {
public:
    void run();

    Game() :/*maze{new MazeState(1,1)},*/ runner{maze}, screenDimensions{} {screenDimensions = ScreenDimensions();}
private:
    int InitSDL();

    void GameInit();

    void OnScreenUpdate();
    void GenerateCellPoints();

    std::vector<std::vector<Point>> cellPoints;
    ScreenDimensions screenDimensions;

    std::shared_ptr<MazeState> maze;
    Runner runner;

    SDL_Window *window;
    SDL_Renderer *renderer;
};
