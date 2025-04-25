package model

import (
	"time"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

type Fault struct {
	ID         primitive.ObjectID `bson:"_id,omitempty" json:"id"`
	ProductID  string             `bson:"product_id"    json:"product_id"`
	FaultType  string             `bson:"fault_type"    json:"fault_type"` // e.g., "crack", "scratch"
	Confidence float64            `bson:"confidence"    json:"confidence"`
	DetectedAt time.Time          `bson:"detected_at"   json:"detected_at"`
	ImageURL   string             `bson:"image_url"     json:"image_url"` // URL ảnh lỗi
}
