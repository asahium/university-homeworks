#define GL_SILENCE_DEPRECATION // Suppress deprecation warnings from OpenGL
#include <GL/glut.h> // Include the GLUT library for cross-platform OpenGL development 

void initializeGL() {
   glClearColor(0.0f, 0.0f, 0.0f, 1.0f); // Set the background color to black (R, G, B, Alpha)
}

void display2() {
   glClear(GL_COLOR_BUFFER_BIT); // Clear the color buffer (background)

   glBegin(GL_TRIANGLES); // Begin drawing a triangle 
      glColor3f(1.0f, 0.0f, 0.0f); // Set color to red for the first vertex
      glVertex2f(0.0f, 0.0f);      // Vertex at the origin (0, 0)

      glColor3f(0.0f, 1.0f, 0.0f); // Set color to green for the second vertex
      glVertex2f(0.5f, 0.0f);      // Vertex at position (0.5, 0) 

      glColor3f(0.0f, 0.0f, 1.0f); // Set color to blue for the third vertex
      glVertex2f(0.0f, 0.5f);      // Vertex at position (0, 0.5)  
   glEnd(); // End the triangle drawing

   glFlush();  // Force any queued OpenGL commands to execute immediately
}


int main(int argc, char** argv) {
   glutInit(&argc, argv);             // Initialize the GLUT library
   glutCreateWindow("Right-Angled Isosceles Triangle"); // Create a window
   glutInitWindowSize(320, 320);      // Set the window's initial width and height
   glutInitWindowPosition(50, 50);    // Set the window's initial position on the screen
   glutDisplayFunc(display2);         // Register 'display2' as the rendering function
   initializeGL();                    // Call the OpenGL initialization function      
   glutMainLoop();                    // Enter the GLUT event loop (never returns)
   return 0;                          // Standard program termination
}

// for compile gcc main.cpp -o main -lGL -lGLU -lglut