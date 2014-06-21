'use strict'

###*
 # @ngdoc function
 # @name etcApp.controller:MainCtrl
 # @description
 # # MainCtrl
 # Controller of the etcApp
###
angular.module('etcApp')
  .controller 'MainCtrl', ($scope) ->
    $scope.awesomeThings = [
      'HTML5 Boilerplate'
      'AngularJS'
      'Karma'
    ]
