GET_STATUS_RESPONSE_EXAMPLES = {
	200: {
		"description": "Connection status returned successfully.",
		"content": {
			"application/json": {
				"example": {
					"athlete_id": 123456,
					"connected": True,
					"needs_refresh": False,
					"expired": False,
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
}