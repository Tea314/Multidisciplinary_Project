package fault

import (
	"context"
	"errors"
	"log"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"

	"fault-detection-backend/internal/model"
)

type Repository interface {
	Create(ctx context.Context, fault *model.Fault) error
	FindByID(ctx context.Context, id string) (*model.Fault, error)
}

type faultRepository struct {
	collection *mongo.Collection
}

func NewRepository(db *mongo.Database) Repository {
	return &faultRepository{
		collection: db.Collection("faults"),
	}
}

func (r *faultRepository) Create(
	ctx context.Context,
	fault *model.Fault,
) error {
	_, err := r.collection.InsertOne(ctx, fault)
	return err
}

func (r *faultRepository) FindByID(
	ctx context.Context,
	id string,
) (*model.Fault, error) {
	log.Printf("Querying fault with ID: %s", id)
	if !primitive.IsValidObjectID(id) {
		log.Printf("Invalid ObjectID: %s", id)
		return nil, errors.New("invalid ObjectID")
	}
	objID, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		log.Printf("Failed to parse ObjectID: %v", err)
		return nil, err
	}
	var fault model.Fault
	err = r.collection.FindOne(ctx, bson.M{"_id": objID}).Decode(&fault)
	if err != nil {
		log.Printf("Fault not found for ID: %s, Error: %v", id, err)
		return nil, err
	}
	log.Printf("Found fault: %+v", fault)
	return &fault, nil
}
