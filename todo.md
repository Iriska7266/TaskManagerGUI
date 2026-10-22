# ToDo list
## Critical
- [x] Create flet page for configuring .env settings;
- [x] Add routing system
- [x] Every user should have his private file with filter (maybe not only filters) settings 

## Identification
- [x] Authorisation
- [x] Registration
- [x] "Remember me" flag

## Tasks
- [x] Main Menu:
- - [x] Adding and editing task with date-time widget (pop-up, right-bottom creation button);
- - [x] Show all tasks (preview);
- - [x] Add filter "Show only active tasks";
- - [x] Add page refresh button;
- - [x] Add "exit from account" button;
- - [x] Delete task;
- - [x] Status hot swap button;
- [x] Task dialog window:
- - [x] Edit title func;
- - [x] Edit content func;
- - [x] Edit deadline func;
- [x] Filters:
- - [x] Add filters values saving on exit from program (and from account);

## Issues
- [x] AuthPage: correct message_field height (or make another type of notification);
- [ ] TasksPage:
- - [x] Edit tasks sorting (query in repository)
- - [ ] task_preview_card:
- - - [ ] Non-clickable text fields;
- - [ ] task_dialog:
- - - [ ] Add seconds choice to deadline time. Now it has only hours and minutes;
- - - [x] Fix program appearance after adding/editing task.
            When task added/updated ResponsiveRow jumps to the start
            (swap full grid reconstruction to specific card updating);
- [x] TaskDTO:
- - [x] Add null-fields support
- [x] TasksPage.banner:
- - [x] Add time to live after which banner will close automatically (about 5 seconds);
- - - [x] Fixed by using Snackbar
- [x] Timezones...: fix creation time factory. Delete function breaks date-times;

## Cosmetics
- [x] TasksPage.task_dialog:
- - [x] Edit text fields style;
- - [x] Edit deadline fields width (with constants or make it adaptive);