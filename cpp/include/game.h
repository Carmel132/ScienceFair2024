#pragma once

#include <SDL.h>

class Game {
public:
    void run();
private:
    int InitSDL();
    void CloseSDL();
    
    SDL_Window *window;
    SDL_Renderer *renderer;
};