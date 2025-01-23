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

    Game() :/*maze{new MazeState(1,1)},*/ runner{maze}, screenDimensions{}, gameRenderer{} {screenDimensions = ScreenDimensions();}
private:
    int InitSDL();

    void GameInit();

    void OnScreenUpdate();
    void OnKeyPress(SDL_Keysym key);

    void next();
    void back();

    ScreenDimensions screenDimensions;
    GameRenderer gameRenderer;
    std::shared_ptr<MazeState> maze;
    Runner runner;
};
