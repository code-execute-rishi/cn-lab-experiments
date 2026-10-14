# ==============================================================================
#   Makefile for Computer Networks Laboratory (CS-504 / CS-501) Experiments 1-9
#   Student: Aradhya Jain  |  Scholar No: 24112011111  |  Section: CSE-1
#   Institution: MANIT Bhopal
# ==============================================================================

CXX = clang++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2
LDFLAGS = -lpthread

BIN_DIR = bin
SRC_DIR = src
TARGET = $(BIN_DIR)/cn_labs_all

.PHONY: all clean run lab1 lab2 lab3 lab4 lab5 lab6 lab7 lab8 lab9 test_python

all: $(TARGET)

$(TARGET): cn_labs_1_to_9.cpp | $(BIN_DIR)
	@echo "==> Compiling master all-in-one C++ binary: $(TARGET)..."
	$(CXX) $(CXXFLAGS) cn_labs_1_to_9.cpp -o $(TARGET) $(LDFLAGS)
	@echo "==> Build successful! Binary located at $(TARGET)"

$(BIN_DIR):
	@mkdir -p $(BIN_DIR)

run: $(TARGET)
	@./$(TARGET) --all

lab1: $(TARGET)
	@./$(TARGET) --lab 1

lab2: $(TARGET)
	@./$(TARGET) --lab 2

lab3: $(TARGET)
	@./$(TARGET) --lab 3

lab4: $(TARGET)
	@./$(TARGET) --lab 4

lab5: $(TARGET)
	@./$(TARGET) --lab 5

lab6: $(TARGET)
	@./$(TARGET) --lab 6

lab7: $(TARGET)
	@./$(TARGET) --lab 7

lab8: $(TARGET)
	@./$(TARGET) --lab 8

lab9: $(TARGET)
	@./$(TARGET) --lab 9

test_python:
	@python3 cn_labs_1_to_9.py --all

clean:
	@echo "==> Cleaning build artifacts..."
	rm -rf $(BIN_DIR)
	@echo "==> Clean complete."
