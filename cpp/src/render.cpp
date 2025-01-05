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