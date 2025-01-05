#pragma once

#include <SDL.h>
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