package main

import (
	"fmt"
	"net/http"
)

// handler function for the "/" route
func helloHandler(w http.ResponseWriter, r *http.Request) {
	// Send a "Hello, World!" response
	fmt.Fprintln(w, "Hello, World!")
}

func main() {
	// Set up a route and link it to the handler
	http.HandleFunc("/", helloHandler)

	// Start the server on port 8080
	fmt.Println("Server is running on http://localhost:8080")
	http.ListenAndServe(":8080", nil)
}
