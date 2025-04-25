package main

import (
	"context"
	"log"

	"github.com/gin-gonic/gin"

	"fault-detection-backend/internal/config"
	"fault-detection-backend/internal/handler"
	"fault-detection-backend/pkg/mongodb"
)

func main() {
	// Load config first
	cfg, err := config.LoadConfig()
	if err != nil {
		log.Fatal("Failed to load config:", err)
	}

	// Connect to MongoDB
	mongoClient, err := mongodb.NewClient(cfg.MongoURI)
	if err != nil {
		log.Fatal("Failed to connect to MongoDB:", err)
	}
	defer mongoClient.Disconnect(context.Background())

	// Initialize router
	r := gin.Default()

	// Setup handlers
	handler.SetupRoutes(r, mongoClient, cfg.DBName)

	for _, route := range r.Routes() {
		log.Printf("Route: %s %s", route.Method, route.Path)
	}
	// Start server
	log.Fatal(r.Run(":" + cfg.Port))
}
