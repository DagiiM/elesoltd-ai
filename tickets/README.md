### Endpoints ###

GET /tickets: Retrieve a list of all tickets
POST /tickets: Create a new ticket
GET /tickets/{id}: Retrieve a specific ticket
PUT /tickets/{id}: Update a specific ticket
DELETE /tickets/{id}: Delete a specific ticket
POST /tickets/{id}/assign_ticket: Assign an assignee to a specific ticket
POST /tickets/{id}/resolve_ticket: Mark a specific ticket as resolved
GET /tickets/{id}/comments: Retrieve all comments for a specific ticket
POST /tickets/{id}/add_comment: Add a new comment to a specific ticket
PUT /tickets/{id}/update_comment: Update an existing comment for a specific ticket
DELETE /tickets/{id}/delete_comment: Delete an existing comment for a specific ticket
GET /ticket-assignees: Retrieve a list of all ticket assignees
POST /ticket-assignees: Create a new ticket assignee
GET /ticket-assignees/{id}: Retrieve a specific ticket assignee
PUT /ticket-assignees/{id}: Update a specific ticket assignee
DELETE /ticket-assignees/{id}: Delete a specific ticket assignee
GET /ticket-assignees/{id}/tickets: Retrieve all tickets assigned to a specific assignee