package fault

import (
	"net/http"

	"github.com/gin-gonic/gin"

	"fault-detection-backend/internal/model"
	"fault-detection-backend/internal/service/fault"
)

type Handler struct {
	service fault.Service
}

func NewHandler(service fault.Service) *Handler {
	return &Handler{service: service}
}

func (h *Handler) CreateFault(c *gin.Context) {
	var fault model.Fault
	if err := c.ShouldBindJSON(&fault); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	err := h.service.CreateFault(c.Request.Context(), &fault)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, fault)
}

func (h *Handler) GetFault(c *gin.Context) {
	id := c.Param("id")
	fault, err := h.service.GetFaultByID(c.Request.Context(), id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Fault not found"})
		return
	}

	c.JSON(http.StatusOK, fault)
}
