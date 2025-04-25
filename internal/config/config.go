package config

import (
	"os"

	"github.com/joho/godotenv"
)

type Config struct {
	MongoURI string
	DBName   string
	Port     string
}

func LoadConfig() (*Config, error) {
	err := godotenv.Load()
	if err != nil {
		return nil, err
	}

	return &Config{
		MongoURI: os.Getenv("MONGODB_URI"),
		DBName:   os.Getenv("DB_NAME"),
		Port:     os.Getenv("PORT"),
	}, nil
}
