#pragma once
#ifdef __linux__
#include "SDL2/SDL.h"
#else
#include "SDL.h"
#endif
#include "render.h"
class Game {
public:
    void run();
private:
    int InitSDL();
    void CloseSDL();

    SDL_Window *window;
    SDL_Renderer *renderer;
};
