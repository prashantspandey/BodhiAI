var _slicedToArray=function(e,n){if(Array.isArray(e))return e;if(Symbol.iterator in Object(e))return function(e,n){var t=[],a=!0,r=!1,o=void 0;try{for(var i,d=e[Symbol.iterator]();!(a=(i=d.next()).done)&&(t.push(i.value),!n||t.length!==n);a=!0);}catch(e){r=!0,o=e}finally{try{!a&&d.return&&d.return()}finally{if(r)throw o}}return t}(e,n);throw new TypeError("Invalid attempt to destructure non-iterable instance")};!function(r){"use strict";var e=r.performance||{},o=e.navigation,t=r.appVars||{},n=r.TTCOM_Scripts||{};n.perfGathering={};var i=e.timing,a=n.splunk,d=n.PromiseHandler,c=n.perfBeaconTools,s=r.analyticsUtility,m=null,u={domInteractiveInMilliseconds:0,domCompleteInMilliseconds:0,perceivedLoadTimeInMicroseconds:0},g={divideDurationBy1000AndRoundTwoDecimals:function(e){return(e/1e3).toFixed(2)},getDifferenceBetweenTimestampsInSeconds:function(e,n){var t=n-e;return g.divideDurationBy1000AndRoundTwoDecimals(t)},getKeyValuePairsStringFromObject:function(e){var r=[];return Object.entries(e).forEach(function(e){var n=_slicedToArray(e,2),t=n[0],a=n[1];r.push(t+"="+a)}),r.join("&")},getExperienceName:function(){var e="",n=document.querySelector("[data-com-type='page']");return t.pageview&&t.pageview.contentIdentifier&&(e=t.pageview.contentIdentifier),n&&n.dataset.autoSel&&(e&&(e+="|"),e+=n.dataset.autoSel),e},getRandomNumberUnder100:function(){return Math.floor(100*Math.random())+1},thisDataShouldBeTracked:function(e){e=e||{};var n=Object.assign({samplingPercentage:0,enabled:!1},e);if(!1===n.enabled||0===Number(n.samplingPercentage))return!1;if(100===Number(n.samplingPercentage))return!0;if(r.localStorage){var t=r.localStorage.getItem("includeInPerfSampling");if("true"===t)return!0;if("false"===t)return!1}var a=g.getRandomNumberUnder100()<=n.samplingPercentage;try{r.localStorage.setItem("includeInPerfSampling",a)}catch(e){}return a}},v=function(){var e,n,t,a=function(e){var n=Object.assign({},e);for(var t in e)e.hasOwnProperty(t)&&(e[t]<=0||isNaN(e[t]))&&delete n[t];return n}((e=i,n=u.perceivedLoadTimeInMicroSeconds,t=g.divideDurationBy1000AndRoundTwoDecimals(n),{navigationStart2loadEventEnd:g.getDifferenceBetweenTimestampsInSeconds(e.navigationStart,e.loadEventEnd),navigationStart2connectEnd:g.getDifferenceBetweenTimestampsInSeconds(e.navigationStart,e.connectEnd),requestStart2responseEnd:g.getDifferenceBetweenTimestampsInSeconds(e.requestStart,e.responseEnd),domLoading2domComplete:g.getDifferenceBetweenTimestampsInSeconds(e.domLoading,e.domComplete),domLoading2domContentLoaded:g.getDifferenceBetweenTimestampsInSeconds(e.domLoading,e.domContentLoaded),loadEventStart2loadEventEnd:g.getDifferenceBetweenTimestampsInSeconds(e.loadEventStart,e.loadEventEnd),navigationStart2domInteractive:g.getDifferenceBetweenTimestampsInSeconds(e.navigationStart,e.domInteractive),navigationStart2perceivedLoadTime:t,connectEnd2domContentLoaded:g.getDifferenceBetweenTimestampsInSeconds(e.connectEnd,e.domContentLoadedEventStart),navigationStart2domContentLoaded:g.getDifferenceBetweenTimestampsInSeconds(e.navigationStart,e.domContentLoadedEventStart),navigationStart2domComplete:g.getDifferenceBetweenTimestampsInSeconds(e.navigationStart,e.domComplete),redirectStart2redirectEnd:g.getDifferenceBetweenTimestampsInSeconds(e.redirectStart,e.redirectEnd),fetchStart2domainLookupStart:g.getDifferenceBetweenTimestampsInSeconds(e.fetchStart,e.domainLookupStart),domainLookupStart2domainLookupEnd:g.getDifferenceBetweenTimestampsInSeconds(e.domainLookupStart,e.domainLookupEnd),connectStart2connectEnd:g.getDifferenceBetweenTimestampsInSeconds(e.connectStart,e.connectEnd),requestStart2responseStart:g.getDifferenceBetweenTimestampsInSeconds(e.requestStart,e.responseStart),unloadEventStart2unloadEventEnd:g.getDifferenceBetweenTimestampsInSeconds(e.unloadEventStart,e.unloadEventEnd),domContentLoadedEventStart2domContentLoadedEventEnd:g.getDifferenceBetweenTimestampsInSeconds(e.domContentLoadedEventStart,e.domContentLoadedEventEnd),domLoading2domInteractive:g.getDifferenceBetweenTimestampsInSeconds(e.domLoading,e.domInteractive)}));return a.navigationType=o.type,a.navigationRedirectCount=o.redirectCount,a.experience=g.getExperienceName(),Object.assign(a,{appCodeName:r.navigator.appCodeName,appName:r.navigator.appName,appVersion:r.navigator.appVersion,concurrentHardware:r.navigator.hardwareConcurrency,oscpu:r.navigator.oscpu,platform:r.navigator.platform,productSub:r.navigator.productSub,userAgent:r.navigator.userAgent,vendor:r.navigator.vendor,vendorSub:r.navigator.vendorSub}),{prettyMessage:"performance data gathered",url:"/api/v1/cse/jsError",logKey:"clientSidePerformanceData",logValue:"data&"+g.getKeyValuePairsStringFromObject(a),cookieIds:"tms,s_vi"}},p=function(){a&&a.logMessage(v())},f=function(){var e="performance|domInteractive";return u.perceivedLoadTimeInMicroSeconds&&(e+="|perceivedLoadTime"),e},l=function(){var e=""+u.domInteractiveInMilliseconds;return u.perceivedLoadTimeInMicroSeconds&&(e+="|"+u.perceivedLoadTimeInMicroSeconds),e},S=function(){if(s){u.domInteractiveInMilliseconds=i.domInteractive-i.navigationStart;var e=f(),n=l();s.triggerEvent("page-perf-event",[{key:"REM",value:n},{key:"EVENT_TYPE",value:e}])}},E=function(){s&&s.triggerEvent("page-perf-event",[{key:"REM",value:i.domComplete-i.navigationStart},{key:"EVENT_TYPE",value:"performance|domComplete"}])};c&&i&&(d&&window.Promise?(m=new d,document.addEventListener("DOMContentLoaded",function(){m.registerCriteria(c.getCriteria()),m.evaluateCriteria().then(function(){1<=m.countCriteria()&&(u.perceivedLoadTimeInMicroSeconds=e.now()),S()})}),window.addEventListener("load",function(){g.thisDataShouldBeTracked(t.perfLogging)&&!Object.is(i,{})&&(setTimeout(p,1e3),E())})):(document.addEventListener("DOMContentLoaded",function(){S()}),document.addEventListener("load",function(){E()})),n.perfGathering.getBeaconDurationName=f,n.perfGathering.getBeaconDurationValue=l)}(window);