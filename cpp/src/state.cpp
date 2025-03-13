#include <state.h>

void MazeState::set(int x, int y, int val) { cells[y][x] = val; }

int MazeState::get(int x, int y) const { return cells[y][x]; }

std::string MazeState::toString() const {
  std::stringstream ss;

  for (int i = 0; i < 2 * height + 1; ++i) {
    std::copy(std::begin(cells[i]), std::end(cells[i]),
              std::ostream_iterator<int>(ss, " "));
    ss << "\n";
  }

  return ss.str();
}

MazeState::MazeState() {
  width = 1;
  height = 1;

  cells = std::vector<std::vector<int>>();
  std::cerr << "Called default maze constructor\n";
}

MazeState::MazeState(int _width, int _height) {
  width = _width;
  height = _height;
  cells = std::vector<std::vector<int>>();
  for (int i = 0; i < 1 + 2 * height; ++i) {
    cells.push_back(std::vector<int>());
    for (int j = 0; j < 1 + 2 * width; ++j) {
      cells[i].push_back((int)!(i % 2 && j % 2));
    }
  }
  std::cerr << "Called maze constructor\n";
}
