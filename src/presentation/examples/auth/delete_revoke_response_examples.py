DELETE_REVOKE_RESPONSE_EXAMPLES = {
	200: {
		"description": "Token revoked successfully.",
		"content": {
			"application/json": {
				"example": {
					"revoked": True,
					"athlete_id": 123456,
				}
			}
		},
	},
	500: {
		"description": "Internal server error.",
		"content": {"application/json": {"example": {"detail": "Failed to revoke token."}}},
	},
}
