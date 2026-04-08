POST_CHAT_RESPONSE_EXAMPLES = {
	201: {
		"description": "Chat response created successfully.",
		"content": {
			"application/json": {
				"example": {
					"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
					"athlete_id": 123456,
					"message": "What was my longest run last month?",
					"response": "Your longest run last month was 21.1 km on March 15th, taking 1h 52m.",
				}
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