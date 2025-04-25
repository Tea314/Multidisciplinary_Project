package main

import (
	"context"
	"log"

	"go.mongodb.org/mongo-driver/bson"

	"fault-detection-backend/internal/config"
	"fault-detection-backend/pkg/mongodb"
)

func main() {
	// Load config
	cfg, err := config.LoadConfig()
	if err != nil {
		log.Fatal("Failed to load config:", err)
	}

	// Connect to MongoDB
	client, err := mongodb.NewClient(cfg.MongoURI)
	if err != nil {
		log.Fatal("Failed to connect to MongoDB:", err)
	}
	defer client.Disconnect(context.Background())

	// Access the faults collection
	collection := client.Database(cfg.DBName).Collection("faults")

	// Query all documents
	ctx := context.Background()
	cursor, err := collection.Find(ctx, bson.M{})
	if err != nil {
		log.Fatal("Failed to query faults:", err)
	}
	defer cursor.Close(ctx)

	// Iterate through results
	var results []bson.M
	if err := cursor.All(ctx, &results); err != nil {
		log.Fatal("Failed to decode results:", err)
	}

	// Print results
	if len(results) == 0 {
		log.Println("No faults found in the collection")
	} else {
		log.Println("Found faults:")
		for _, result := range results {
			log.Printf("ID: %s, Data: %+v\n", result["_id"], result)
		}
	}
}
