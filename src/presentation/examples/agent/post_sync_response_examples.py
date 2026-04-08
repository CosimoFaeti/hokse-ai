POST_SYNC_RESPONSE_EXAMPLES = {
	201: {
		"description": "Activities synced successfully.",
		"content": {
			"application/json": {
				"example": [
					{
						"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
						"athlete_id": 123456,
						"name": "Morning Run",
						"distance": 10234.5,
						"moving_time": 3600,
						"elapsed_time": 3720,
						"sport_type": "Run",
					}
				]
			}
		},
	},
	422: {
		"description": "Validation error.",
		"content": {
			"application/json": {
				"example": {"detail": "Validation error."}
			}
		},
	},
	500: {
		"description": "Internal server error.",
		"content": {
			"application/json": {
				"example": {"detail": "Internal server error."}
			}
		},
	},
}