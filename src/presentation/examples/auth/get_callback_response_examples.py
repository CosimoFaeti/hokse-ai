GET_CALLBACK_RESPONSE_EXAMPLES = {
	302: {
		"description": "OAuth exchange successful, redirecting to Streamlit.",
		"content": {
			"application/json": {
				"example": {"detail": "Redirecting to application..."}
			}
		},
	},
	400: {
		"description": "Invalid OAuth state parameter.",
		"content": {
			"application/json": {
				"example": {"detail": "Invalid OAuth state parameter."}
			}
		},
	},
	502: {
		"description": "Failed to exchange authorisation code.",
		"content": {
			"application/json": {
				"example": {"detail": "Failed to exchange Strava authorisation code."}
			}
		},
	},
}