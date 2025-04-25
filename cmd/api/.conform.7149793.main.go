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
	handler.SetupRouters(r, mongoClient, cfg.DBName)

	// Start server
	log.Fatal(r.Run(":" + cfg.Port))
}
