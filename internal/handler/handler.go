package handler

import (
	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/mongo"

	faultHandler "fault-detection-backend/internal/handler/fault" // Import handler/fault
	faultRepo "fault-detection-backend/internal/repository/fault" // Import repository/fault
	faultService "fault-detection-backend/internal/service/fault"
)

func SetupRoutes(r *gin.Engine, client *mongo.Client, dbName string) {
	db := client.Database(dbName)

	// Initialize repositories
	faultRepoInstance := faultRepo.NewRepository(db)

	// Initialize services
	faultServiceInstance := faultService.NewService(faultRepoInstance)

	// Initialize handlers
	faultHandler := faultHandler.NewHandler(faultServiceInstance)

	// Define routes
	v1 := r.Group("/api/v1")
	{
		v1.POST("/faults", faultHandler.CreateFault)
		v1.GET("/faults/:id", faultHandler.GetFault)
	}
}
