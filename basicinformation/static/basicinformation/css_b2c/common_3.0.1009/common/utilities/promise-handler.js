var _createClass=function(){function n(e,t){for(var r=0;r<t.length;r++){var n=t[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}return function(e,t,r){return t&&n(e.prototype,t),r&&n(e,r),e}}();function _classCallCheck(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}window.TTCOM_Scripts=window.TTCOM_Scripts||{},window.TTCOM_Scripts.PromiseHandler=function(){function t(e){_classCallCheck(this,t),this._criteria=[],this.promiseHandlerNameSpace=e,this.promiseRejectedReason=void 0,this._events={}}return _createClass(t,[{key:"createEvents",value:function(){window.Event&&(this._events.resolved=new Event(this.promiseHandlerNameSpace+".performanceBeaconPromisesResolved")),window.CustomEvent?this._events.rejected=new CustomEvent(this.promiseHandlerNameSpace+".performanceBeaconPromisesRejected",{detail:this.promiseRejectedReason}):window.Event&&(this._events.rejected=new Event(this.promiseHandlerNameSpace+".performanceBeaconPromisesRejected"))}},{key:"registerCriterion",value:function(e){var t=!1;return e instanceof Promise&&(t=!0,this._criteria.push(e)),t}},{key:"registerCriteria",value:function(e){var t=this;e.forEach(function(e){t.registerCriterion(e)})}},{key:"evaluateCriteria",value:function(){var t=this;return Promise.all(this._criteria).then(function(){t._events.resolved&&document.dispatchEvent(t._events.resolved)}).catch(function(e){t.promiseRejectedReason=e,t._events.rejected&&document.dispatchEvent(t._events.rejected)})}},{key:"resetCriteria",value:function(){return this._criteria=[],this.countCriteria()}},{key:"countCriteria",value:function(){return this._criteria.length}}]),t}();