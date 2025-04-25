package fault

import (
	"context"

	"fault-detection-backend/internal/model"
	"fault-detection-backend/internal/repository/fault"
)

type Service interface {
	CreateFault(ctx context.Context, fault *model.Fault) error
	GetFaultByID(ctx context.Context, id string) (*model.Fault, error)
}

type faultService struct {
	repo fault.Repository
}

func NewService(repo fault.Repository) Service {
	return &faultService{repo: repo}
}

func (s *faultService) CreateFault(
	ctx context.Context,
	fault *model.Fault,
) error {
	return s.repo.Create(ctx, fault)
}

func (s *faultService) GetFaultByID(
	ctx context.Context,
	id string,
) (*model.Fault, error) {
	return s.repo.FindByID(ctx, id)
}
