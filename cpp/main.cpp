#include "SDL.h"
#include "test.h"
#include <iostream>
SDL_Window *Window;
SDL_Renderer *Renderer;

int Init()
{
    int Success = 1;
    
    if(SDL_Init(SDL_INIT_VIDEO) != 0)
    {
        SDL_Log("Failed to initialize SDL! SDL_GetError: %s\n", SDL_GetError());
        Success = 0;
    }
    else
    {
        Window = SDL_CreateWindow("SDL Test",
                                  SDL_WINDOWPOS_UNDEFINED,
                                  SDL_WINDOWPOS_UNDEFINED,
                                  640,
                                  480,
                                  0);    
        if(!Window)
        {
            SDL_Log("Failed to create window! SDL_GetError: %s\n", SDL_GetError());
            Success = 0;
        }
        else
        {
            Renderer = SDL_CreateRenderer(Window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
            if(!Renderer)
            {
                SDL_Log("Failed to create renderer!\n");
                Success = 0;
            }
            else
            {   
                SDL_SetRenderDrawColor(Renderer, 0xff, 0xff, 0xff, 0xff);
				
		
            }
        }
    }
    
    return Success;
}

int main(int argc, char *argv[])
{
    std::cout << C{}.m();
    if(!Init())
    {
        SDL_Log("Failed to initalize!\n");
    }
    else
    {
        int Running = 1;
        SDL_Event e;
        
        while(Running)
        {
            while(SDL_PollEvent(&e) != 0)
            {
                if(e.type == SDL_QUIT)
                {
                    Running = 0;
                }
            }
            
            SDL_SetRenderDrawColor(Renderer, 0xff, 0, 0, 0xff);
            SDL_RenderClear(Renderer);
            
            SDL_RenderPresent(Renderer);
        }
    }
    
    // Shutdown
    SDL_DestroyRenderer(Renderer);
    SDL_DestroyWindow(Window);
	Renderer = NULL;
    Window =  NULL;
    
    SDL_Quit();
    return 0;
}