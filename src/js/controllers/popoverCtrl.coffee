angular.module('Courses.controllers')
.controller 'popoverCtrl', (
  $scope,
  $rootScope,
  $timeout,
) ->
  popoverShown = false
  $scope.removeCourse = (course) ->
    $scope.schedule.removeCourse course
    $scope.hide()

  $scope.changeSections = (course) ->
    $scope.schedule.removeCourse course
    for section in course.selectedSections
      section.selected = false
    course.selectedSections = []
    $scope.schedule.addCourse course
    $scope.hide()

  $scope.$on 'sectionClicked', (event, section) ->
    if section.id is $scope.course.id and not popoverShown
      $timeout () ->
        $scope.show()


  # Handle clicks outside of the popover so the popover closes
  $scope.$on 'popover-shown', (ev) ->
    popoverShown = true
    $(document).on 'click.hidepopover', (event) ->
      if not $(event.target).parents().filter('.courseBlock').length
        # Click outside the popover
        $scope.hide()

  $scope.$on 'popover-hide', (ev) ->
    popoverShown = false
    $(document).off 'click.hidepopover'