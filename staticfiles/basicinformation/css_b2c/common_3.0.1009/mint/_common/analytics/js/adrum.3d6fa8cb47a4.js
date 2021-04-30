var _typeof="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t};new function(){if(!window.ADRUM&&!0!==window["adrum-disable"]){var t=window.ADRUM={};window["adrum-start-time"]=window["adrum-start-time"]||(new Date).getTime(),((xt=t||(t={})).monitor||(xt.monitor={})).ed=function(){for(var t=[],e=0;e<arguments.length;e++)t[e-0]=arguments[e];for(e=0;e<t.length;e++){var n=t[e];n&&n.setUp()}},function(t){(t=t.conf||(t.conf={})).beaconUrlHttp="http://col.eum-appdynamics.com",t.beaconUrlHttps="https://col.eum-appdynamics.com",t.corsEndpointPath="/eumcollector/beacons/browser/v1",t.imageEndpointPath="/eumcollector/adrum.gif?",t.appKey=window["adrum-app-key"]||"AD-AAB-AAF-BVV";var e="https:"===document.location.protocol;if(t.adrumExtUrl=(e?"https://cdn.appdynamics.com":"http://cdn.appdynamics.com")+"/adrum-ext.206c403a1a532b310b15ea4509f4902b.js",t.adrumXdUrl="https://cdn.appdynamics.com/adrum-xd.206c403a1a532b310b15ea4509f4902b.html",t.agentVer="4.2.15.3",t.sendImageBeacon="false",window["adrum-geo-resolver-url"]){var n=window["adrum-geo-resolver-url"],r=n.indexOf("://");-1!=r&&(n=n.substring(r+3)),n=(e?"https://":"http://")+n}else n="";t.geoResolverUrl=n,t.useStrictDomainCookies=!0===window["adrum-use-strict-domain-cookies"],t.userConf=window["adrum-config"],t.fe=10}(t||(t={})),function(n){function r(t){return null!=t}function a(t){return"[object Array]"===Object.prototype.toString.apply(t)}function s(t){return"object"==(void 0===t?"undefined":_typeof(t))&&!a(t)&&null!==t}function e(t){return"string"==typeof t}function u(t,e){return Object.prototype.hasOwnProperty.call(t,e)&&r(t[e])}function c(t){return e(t)?t.replace(/^\s*/,"").replace(/\s*$/,""):t}n.isDefined=r,n.isArray=a,n.isObject=s,n.isFunction=function(t){return"function"==typeof t||!1},n.isString=e,n.isNumber=function(t){return"number"==typeof t},n.Xa=function(t){setTimeout(t,0)},n.addEventListener=function(e,n,t){function r(){try{return t.apply(this,Array.prototype.slice.call(arguments))}catch(t){Et.exception(t,"M1",n,e,t)}}Et.isDebug&&Et.log("M0",n,e),e.addEventListener?e.addEventListener(n,r,!1):e.attachEvent&&e.attachEvent("on"+n,r)},n.loadScriptAsync=function(t){var e=document.createElement("script");e.async=!0,e.src=t;var n=document.getElementsByTagName("script")[0];n?(n.parentNode.insertBefore(e,n),Et.log("M2",t)):Et.log("M3",t)},n.mergeJSON=function t(e,n){for(var r in n){var o=n[r];if(u(n,r)){var i=e[r];s(o)&&s(i)?t(i,o):e[r]=a(i)&&a(o)?i.concat(o):o}}return e},n.hasOwnPropertyDefined=u,n.ud=function(t){var e=[];return t&&(n.isObject(t)?e=[t]:n.isArray(t)&&(e=t)),e},n.generateGUID=void 0!==window.crypto&&void 0!==window.crypto.getRandomValues?function(){function t(t){for(t=t.toString(16);t.length<4;)t="0"+t;return t}var e=new Uint16Array(8);return window.crypto.getRandomValues(e),t(e[0])+t(e[1])+"_"+t(e[2])+"_"+t(e[3])+"_"+t(e[4])+"_"+t(e[5])+t(e[6])+t(e[7])}:function(){return"xxxxxxxx_xxxx_4xxx_yxxx_xxxxxxxxxxxx".replace(/[xy]/g,function(t){var e=16*Math.random()|0;return("x"==t?e:3&e|8).toString(16)})},n.md=function(t){return t&&(t=t.stack)&&"string"==typeof t?t:null},n.trim=c,n.Eg=function(t){var e,n,r={};if(!t)return r;var o=t.split("\n");for(n=0;n<o.length;n++){var i=o[n];e=i.indexOf(":"),t=c(i.substr(0,e)).toLowerCase(),e=c(i.substr(e+1)),t&&(r[t]=r[t]?r[t]+", "+e:e)}return r},n.tryPeriodically=function(n,r,o,i){var a=0;!function t(){if(r())o&&o();else{var e=n(++a);0<e?setTimeout(t,e):i&&i()}}()},n.Vb=function(t){return t.charAt(0).toUpperCase()+t.slice(1)},n.Nc=function(n){for(var r=[],t=1;t<arguments.length;t++)r[t-1]=arguments[t];return function(){for(var t=[],e=0;e<arguments.length;e++)t[e-0]=arguments[e];return n.apply(this,r.concat(t))}},n.now=Date&&Date.now||function(){return(new Date).getTime()}}((Et=t||(t={})).utils||(Et.utils={})),function(o){function n(t,e,n,r){return t=o.conf.beaconUrlHttps+"/eumcollector/error.gif?version=1&appKey="+n+"&msg="+encodeURIComponent(t.substring(0,500)),r&&(t+="&stack=",t+=encodeURIComponent(r.substring(0,1500-t.length))),t}function r(t,e){2<=a||(document.createElement("img").src=n(t,0,o.conf.appKey,e),a++)}function t(t){return 0<=t.location.search.indexOf("ADRUM_debug=true")||0<=t.cookie.search(/(^|;)\s*ADRUM_debug=true/)}o.iDR=t,o.isDebug=t(document);var i=[];o.logMessages=i,o.log=function(t){for(var e=1;e<arguments.length;e++);o.isDebug&&i.push(Array.prototype.slice.call(arguments).join(" | "))},o.error=function(t){for(var e=1;e<arguments.length;e++);e=Array.prototype.slice.call(arguments).join(" | "),o.log(e),r(e,null)},o.exception=function(){for(var t=[],e=0;e<arguments.length;e++)t[e-0]=arguments[e];arguments.length<1||(t=Array.prototype.slice.call(arguments),e=o.utils.md(t[0]),t=t.slice(1).join(" | "),o.log(t),r(t,e))},o.assert=function(t,e){t||o.error("Assert fail: "+e)},o.dumpLog=o.isDebug?function(){for(var t="",e=0;e<i.length;e++)t+=i[e].replace(RegExp("<br/>","g"),"\n\t")+"\n";return t}:function(){},o.cIEBU=n;var a=0;o.log("M4")}(t||(t={})),bt=t||(t={}),wt=function(){function t(t){this.max=t,this.Ba=0}return t.prototype.Tf=function(){this.ka()||this.Ba++},t.prototype.ka=function(){return this.Ba>=this.max},t.prototype.reset=function(){this.Ba=0},t}(),Tt=function(){function t(){this.ga=[],this.$a=new wt(t.ue),this.Na=new wt(t.ie)}return t.prototype.submit=function(t){this.push(t)&&bt.initEXTDone&&this.processQ()},t.prototype.processQ=function(){for(var t=this.mf(),e=0;e<t.length;e++){var n=t[e];"function"==typeof bt.commands[n[0]]?(bt.isDebug&&bt.log("M5",n[0],n.slice(1).join(", ")),bt.commands[n[0]].apply(bt,n.slice(1))):bt.error("M6",n[0])}},t.prototype.hg=function(t){return"reportXhr"===t||"reportPageError"===t},t.prototype.push=function(t){var e=t[0],n=this.hg(e),r=n?this.$a:this.Na;return r.ka()?(bt.log("M7",n?"spontaneous":"non spontaneous",e),!1):(this.ga.push(t),r.Tf(),!0)},t.prototype.mf=function(){var t=this.ga;return this.reset(),t},t.prototype.size=function(){return this.ga.length},t.prototype.reset=function(){this.ga=[],this.$a.reset(),this.Na.reset()},t.prototype.isSpontaneousQueueDead=function(){return this.$a.ka()},t.prototype.isNonSpontaneousQueueDead=function(){return this.Na.ka()},t.ue=100,t.ie=100,t}(),bt.Id=Tt,(yt=t||(t={})).q=new yt.Id,yt.command=function(t){for(var e=1;e<arguments.length;e++);yt.isDebug&&yt.log("M8",t,Array.prototype.slice.call(arguments).slice(1).join(", ")),yt.q.submit(Array.prototype.slice.call(arguments))},mt=t||(t={}),gt=mt.monitor||(mt.monitor={}),vt=function(){function t(){this.status={}}return t.prototype.setUp=function(){},t.prototype.set=function(t,e){this.status[t]=e},t}(),gt.rb=vt,dt=t||(t={}),ht=dt.aop||(dt.aop={}),(window.ADRUM.aop=ht).support=function(t){return!t||"apply"in t},ht.around=function(r,o,i,a,s){return dt.assert(ht.support(r),"aop.around called on a function which does not support interception"),r=r||function(){},function(){dt.isDebug&&dt.log("M9",a,Array.prototype.slice.call(arguments).join(", "));var t,e=Array.prototype.slice.call(arguments);try{o&&(t=o.apply(this,e))}catch(t){dt.exception(t,"M10",a,t)}dt.assert(!t||"[object Array]"===Object.prototype.toString.call(t));var n=void 0;try{n=r.apply(this,t||e)}catch(t){throw s&&s(t),t}finally{try{i&&i.apply(this,e)}catch(t){dt.exception(t,"M11",a,t)}}return n}},ht.before=function(t,e){return ht.around(t,e)},ht.after=function(t,e){return ht.around(t,null,e)},(pt=(pt=t||(t={})).EventType||(pt.EventType={}))[pt.BASE_PAGE=0]="BASE_PAGE",pt[pt.IFRAME=1]="IFRAME",pt[pt.XHR=2]="XHR",pt[pt.VIRTUAL_PAGE=3]="VIRTUAL_PAGE",pt[pt.PAGE_ERROR=4]="PAGE_ERROR",pt[pt.ABSTRACT=100]="ABSTRACT",pt[pt.ADRUM_XHR=101]="ADRUM_XHR",pt[pt.NG_VIRTUAL_PAGE=102]="NG_VIRTUAL_PAGE",(lt=(lt=t||(t={})).events||(lt.events={})).l={},lt.l[100]={guid:"string",url:"string",parentGUID:"string",parentUrl:"string",parentType:"number",timestamp:"number"},lt.l[3]={resTiming:"object"},lt.l[102]={digestCount:"number"},lt.l[2]={method:"string",parentPhase:"string",parentPhaseId:"number",error:"object"},lt.l[101]={xhr:"object"},lt.l[4]={msg:"string",line:"number",stack:"string"},rt=t||(t={}),ft=function(){function t(){this.w={}}return t.prototype.mark=function(t,e){ot.mark.apply(this,arguments)},t.prototype.getTiming=function(t){return(t=this.getEntryByName(t))&&t.startTime},t.prototype.measure=function(t,e,n){ot.measure.apply(this,arguments)},t.prototype.getEntryByName=function(t){return ot.getEntryByName.call(this,t)},t.Aa=function(t){return ot.Aa(t)},t}(),rt.PerformanceTracker=ft,it=ot||(ot={}),at=rt.utils.hasOwnPropertyDefined,st=window.performance||window.mozPerformance||window.msPerformance||window.webkitPerformance,ut=st&&st.timing&&st.timing.navigationStart?st.timing.navigationStart:window["adrum-start-time"],ct=rt.utils.now,it.mark=function(t,e){this.w[t]={name:t,entryType:"mark",startTime:rt.utils.isDefined(e)?e:ct(),duration:0}},it.measure=function(t,e,n){at(this.w,e)&&at(this.w,n)?this.w[t]={name:t,entryType:"measure",startTime:e?this.w[e].startTime:ut,duration:(n?this.w[n].startTime:ct())-(e?this.w[e].startTime:ut)}:rt.error("M12",at(this.w,e)?n:e)},it.getEntryByName=function(t){return this.w[t]||null},it.Aa=function(t){return t+ut},function(t){function e(t,e){for(var n in t=t||{})e[n]=function(){var r=n,o=t[n];return function(t){var e="_"+r,n=this[e];if(nt.utils.isDefined(t)){if((void 0===t?"undefined":_typeof(t))!==o)throw TypeError("wrong type of "+r+" value, "+(void 0===t?"undefined":_typeof(t))+" passed in but should be a "+o+".");this[e]=t}return n}}()}var n=function(){function t(t){this.perf=new nt.PerformanceTracker,this.timestamp(nt.utils.now()),this.guid(nt.utils.generateGUID()),this.url(document.URL),this.dd(t)}return t.prototype.type=function(){return 100},t.prototype.dd=function(t){if(nt.utils.isObject(t))for(var e in t){var n=this[e]||this["mark"+nt.utils.Vb(e)];n&&nt.utils.isFunction(n)&&n.call(this,t[e])}},t.Rb=function(t,e,n){return{guid:function(){return t},url:function(){return e},type:function(){return n}}},t.prototype.Jf=function(){return t.Rb(this.parentGUID(),this.parentUrl(),this.parentType())},t.prototype.parent=function(t){var e=this.Jf();return nt.utils.isDefined(t)&&(this.parentGUID(t.guid()),this.parentUrl(t.url()),this.parentType(t.type())),e},t}();t.EventTracker=n,t.V=e,t.Sb=function(t,e){var n,r=function(t){var e,n={};for(e in t){var r=t[e];n[r.start]=!0,n[r.end]=!0}return n}(t=t||{});for(n in r)e["mark"+(r=nt.utils.Vb(n))]=nt.utils.Nc(function(t,e){this.perf.mark(t,e)},n),e["get"+r]=nt.utils.Nc(function(t){return this.perf.getTiming(t)},n)},e(t.l[100],n.prototype)}((nt=t||(t={})).events||(nt.events={}));var n=this.Ne||function(t,e){function n(){this.constructor=t}for(var r in e)e.hasOwnProperty(r)&&(t[r]=e[r]);n.prototype=e.prototype,t.prototype=new n};z=t||(t={}),tt=z.events||(z.events={}),et=function(e){function t(t){e.call(this,t)}return n(t,e),t.prototype.type=function(){return 4},t}(tt.EventTracker),tt.Error=et,tt.V(tt.l[4],et.prototype),J=t||(t={}),W=J.monitor||(J.monitor={}),K=function(e){function a(){e.apply(this,arguments)}return n(a,e),a.prototype.setUp=function(){var t=this;e.prototype.setUp.call(this),J.listenForErrors=function(){t.Fc()},this.Fc()},a.prototype.Uc=function(t,e,n,r){a.errorsSent>=J.conf.fe?J.log("M13"):(r=J.utils.md(r),J.command("reportPageError",new J.events.Error(J.utils.mergeJSON({msg:t+"",url:J.utils.isString(e)?e:void 0,line:J.utils.isNumber(n)?n:void 0,stack:r},this.status))),a.errorsSent++)},a.prototype.Fc=function(){var i=this;J.aop.support(window.onerror)?(window.onerror=J.aop.around(window.onerror,function(t,e,n,r,o){a.La||(i.Uc(t,e,n,o),a.La=!0)},function(){a.La=!1},"onerror"),J.log("M14")):J.log("M15")},a.La=!1,a.errorsSent=0,a}(W.rb),W.ErrorMonitor=K,W.Fa=new W.ErrorMonitor,Q=t||(t={}),Y=function(){function r(){this.sa=[],this.na(r.wa,0)}return r.prototype.wg=function(t){this.na(r.Lb,t)},r.prototype.yg=function(t){this.na(r.Tb,t)},r.prototype.xg=function(t){this.na(r.Nb,t)},r.prototype.na=function(t,e){this.sa.push({vg:(new Date).getTime(),ug:e,Oc:t}),this.gf=t},r.prototype.getPhaseName=function(){return this.gf},r.prototype.getPhaseID=function(t){for(var e=0;e<r.Qb.length;e++)if(r.Qb[e]===t)return e;return null},r.prototype.getPhaseCallbackTime=function(t){for(var e=this.sa,n=0;n<e.length;n++)if(e[n].Oc===t)return e[n].vg;return null},r.prototype.findPhaseAtNominalTime=function(t){Q.assert(0<=t);for(var e=this.sa,n=e.length-1;0<=n;n--)if(t>=e[n].ug)return e[n].Oc;return Q.error("M16",t,Q.utils.nf(e)),r.wa},r.Qb=[r.wa="AFTER_FIRST_BYTE",r.Lb="AFTER_DOM_INTERACTIVE",r.Tb="AT_ONLOAD",r.Nb="AFTER_ONLOAD"],r}(),Q.yh=Y,Q.lifecycle=new Y,Q.lifecycle=Q.lifecycle,G=t||(t={}),H=G.events||(G.events={}),Z=function(t){function e(){t.apply(this,arguments)}return n(e,t),e.prototype.type=function(){return 0},e}(H.EventTracker),H.PageView=Z,B=t||(t={}),q=B.monitor||(B.monitor={}),F=function(){function n(){}return n.prototype.setUp=function(){n.Ug(),n.Tg()},n.Tg=function(){B.utils.addEventListener(window,"load",n.oa),B.utils.addEventListener(window,"load",n.Bg)},n.Bg=function(t){B.lifecycle.yg(t&&t.timeStamp),B.utils.Xa(function(){var t=(new Date).getTime();B.lifecycle.xg(t),B.command("mark","onload",t),q.Db.perf&&(q.perfMonitor.cf(),q.perfMonitor.df()),B.command("reportOnload",new B.events.PageView),B.utils.loadScriptAsync(B.conf.adrumExtUrl)}),B.log("M17")},n.Ug=function(){if(document.addEventListener)document.addEventListener("DOMContentLoaded",n.ba,!1);else{document.attachEvent("onreadystatechange",n.ba);var t=null;try{t=null===window.frameElement?document.documentElement:null}catch(t){}null!=t&&t.doScroll&&function e(){if(!n.isReady){try{t.doScroll("left")}catch(t){return void setTimeout(e,10)}n.oa()}}()}B.log("M18")},n.oa=function(t){n.Ic||(B.lifecycle.wg(t&&t.timeStamp),B.command("mark","onready",(new Date).getTime()),n.Ic=!0)},n.ba=function(t){document.addEventListener?(document.removeEventListener("DOMContentLoaded",n.ba,!1),n.oa(t)):"complete"===document.readyState&&(document.detachEvent("onreadystatechange",n.ba),n.oa(t))},n.isReady=!1,n.Ic=!1,n}(),q.Kd=F,q.lf=new q.Kd,N=t||(t={}),O=N.monitor||(N.monitor={}),I=function(){function o(){this.navTiming=this.resTiming=null}return o.prototype.setUp=function(){o.perf=window.performance||window.mozPerformance||window.msPerformance||window.webkitPerformance},o.prototype.cf=function(){var t=o.perf;if(t=t&&t.timing)if(t.navigationStart&&t.navigationStart<=t.loadEventEnd){var e,n={};for(e in t){var r=t[e];"number"==typeof r&&(n[e]=r)}this.navTiming=n}else N.log("M20");else N.log("M19")},o.prototype.df=function(){this.resTiming=this.nc()},o.prototype.nc=function(){var t=o.perf,e=[];return t&&t.getEntriesByType&&(t=t.getEntriesByType("resource"))&&t.length&&0<t.length&&t.unshift&&(e=t),0==e.length&&N.log("M21"),e},o.perf=null,o}(),O.Db=I,O.perfMonitor=new O.Db,V=t||(t={}),($=V.utils||(V.utils={})).parseURI=function(t){var e=String(t).replace(/^\s+|\s+$/g,"").match(/^([^:\/?#]+:)?(?:\/\/(?:([^:@\/?#]*)(?::([^:@\/?#]*))?@)?(([^:\/?#]*)(?::(\d*))?))?([^?#]*)(\?[^#]*)?(#[\s\S]*)?/);return t=e&&null!=t.match(e[1]+"//"),e&&{href:e[0]||"",protocol:e[1]||"",Za:t?"//":"",ib:e[2]||"",Ra:e[3]||"",host:e[4]||"",hostname:e[5]||"",port:e[6]||"",pathname:e[7]||"",search:e[8]||"",hash:e[9]||""}},$.absolutizeURI=function(t,e){function n(t){var e=[];return t.replace(/^(\.\.?(\/|$))+/,"").replace(/\/(\.(\/|$))+/g,"/").replace(/\/\.\.$/,"/../").replace(/\/?[^\/]*/g,function(t){"/.."===t?e.pop():e.push(t)}),e.join("").replace(/^\//,"/"===t.charAt(0)?"/":"")}var r,o,i,a,s,u,c,f;return f=e?$.parseURI(e):{},c=t?$.parseURI(t):{},c=f.protocol?(r=f.protocol,o=f.Za,i=f.ib,a=f.Ra,s=f.host,u=n(f.pathname),f.search):f.host?(r=c.protocol,o=c.Za,i=f.ib,a=f.Ra,s=f.host,u=n(f.pathname),f.search):(r=c.protocol,o=c.Za,i=c.ib,a=c.Ra,s=c.host,f.pathname?(u="/"===f.pathname.charAt(0)?n(f.pathname):n(u=c.pathname?c.pathname.slice(0,c.pathname.lastIndexOf("/")+1)+f.pathname:o?"/"+f.pathname:f.pathname),f.search):(u=n(c.pathname),f.search||c.search)),r+o+(i?i+(a?":"+a:"")+"@":"")+s+u+c+(f.hash?f.hash:"")},$.getFullyQualifiedUrl=function(e){try{var n,t,r=document.location.href;t:{for(var o=document.getElementsByTagName("base"),i=0;i<o.length;i++){var a=o[i].href;if(a){t=a;break t}}t=void 0}return n=t?$.absolutizeURI(r,t):r,$.absolutizeURI(n,e)}catch(t){return V.exception(t,"M22",e,n),e}},(j=(j=(j=t||(t={})).events||(j.events={})).b||(j.b={})).navigationStart="navigationStart",j.domainLookupStart="domainLookupStart",j.domainLookupEnd="domainLookupEnd",j.connectStart="connectStart",j.secureConnectionStart="secureConnectionStart",j.connectEnd="connectEnd",j.requestStart="requestStart",j.responseStart="responseStart",j.responseEnd="responseEnd",j.domContentLoadedEventStart="domContentLoadedEventStart",j.loadEventEnd="loadEventEnd",j.bd="sendTime",j.fc="firstByteTime",j.Yc="respAvailTime",j.Zc="respProcTime",j.jb="viewChangeStart",j.qd="viewChangeEnd",j.kb="viewDOMLoaded",j.wd="xhrRequestsCompleted",j.ei="viewFragmentsLoaded",j.fi="viewResourcesLoaded",j.lb="virtualPageStart",j.nh="virtualPageEnd",(_=(_=t||(t={})).events||(_.events={})).B={},_.B[0]={sf:{start:_.b.navigationStart,end:_.b.loadEventEnd,name:"PLT"},xf:{start:_.b.navigationStart,end:_.b.responseStart,name:"FBT"},ai:{start:_.b.navigationStart,end:_.b.requestStart,name:"SCT"},bi:{start:_.b.secureConnectionStart,end:_.b.connectEnd,name:"SHT"},Ih:{start:_.b.domainLookupStart,end:_.b.domainLookupEnd,name:"DLT"},di:{start:_.b.connectStart,end:_.b.connectEnd,name:"TCP"},Zh:{start:_.b.requestStart,end:_.b.responseStart,name:"RAT"},Kh:{start:_.b.responseStart,end:_.b.loadEventEnd,name:"FET"},Mh:{start:_.b.responseStart,end:_.b.domContentLoadedEventStart,name:"DRT"},Ch:{start:_.b.responseStart,end:_.b.responseEnd,name:"DDT"},Gh:{start:_.b.responseEnd,end:_.b.domContentLoadedEventStart,name:"DPT"},Yh:{start:_.b.domContentLoadedEventStart,end:_.b.loadEventEnd,name:"PRT"},Hh:{start:_.b.navigationStart,end:_.b.domContentLoadedEventStart,name:"DOM"}},_.B[2]={xf:{start:_.b.bd,end:_.b.fc,name:"FBT"},Lh:{start:_.b.fc,end:_.b.Yc,name:"DDT"},Bh:{start:_.b.Yc,end:_.b.Zc,name:"DPT"},sf:{start:_.b.bd,end:_.b.Zc,name:"PLT"}},_.B[3]={Sh:{start:_.b.lb,end:_.b.nh,name:"PLT"},Eh:{start:_.b.jb,end:_.b.qd,name:"DDT"},Ph:{start:_.b.jb,end:_.b.kb,name:"DRT"},th:{start:_.b.qd,end:_.b.kb,name:"DPT"},uh:{start:_.b.jb,end:_.b.kb,name:"DOM"},Xh:{start:"viewChangeEnd",end:"xhrRequestsCompleted",name:null},Qh:{start:"viewChangeEnd",end:"viewPartialsLoaded",name:null},Oh:{start:"viewPartialsLoaded",end:"viewFragmentsLoaded",name:null},Rh:{start:"viewPartialsLoaded",end:"viewResourcesLoaded",name:null}},_.B[102]=_.B[3],D=t||(t={}),U=D.events||(D.events={}),X=function(e){function t(t){e.call(this,t)}return n(t,e),t.prototype.type=function(){return 2},t}(U.EventTracker),U.Ajax=X,U.V(U.l[2],X.prototype),U.Sb(U.B[2],X.prototype),k=t||(t={}),P=k.events||(k.events={}),L=function(e){function t(t){e.call(this,t)}return n(t,e),t.prototype.type=function(){return 2},t}(P.Ajax),P.AdrumAjax=L,P.V(P.l[101],L.prototype),M=t||(t={}),A=M.monitor||(M.monitor={}),C=function(t){function a(){t.call(this),this.conf=null,this.ab=!1,!(this.xa=0)===window["adrum-xhr-disable"]?M.log("M23"):window.XMLHttpRequest?(this.conf={exclude:[{urls:[{pattern:M.conf.beaconUrlHttp+M.conf.corsEndpointPath},{pattern:M.conf.beaconUrlHttps+M.conf.corsEndpointPath}]}],include:[],maxPerPageView:Number.MAX_VALUE},a.Rc(this.conf,M.conf.userConf&&M.conf.userConf.xhr),(this.d=window.XMLHttpRequest.prototype)?"open"in this.d&&"send"in this.d?(this.ab=M.aop.support(this.d.open)&&M.aop.support(this.d.send))||M.log("M27"):M.log("M26"):M.log("M25")):M.log("M24")}return n(a,t),a.Rc=function(t,e){e&&(e.include=M.utils.ud(e.include),e.exclude=M.utils.ud(e.exclude),M.utils.mergeJSON(t,e));var n=t.exclude;if(n)for(var r=0;r<n.length;r++){var o=n[r].urls;o&&0<o.length&&(n[r].urls=a.Zb(o))}if(n=t.include)for(r=0;r<n.length;r++)(o=n[r].urls)&&0<o.length&&(n[r].urls=a.Zb(o));(!M.utils.isNumber(t.maxPerPageView)||t.maxPerPageView<=0)&&(M.log("M28"),t.maxPerPageView=Number.MAX_VALUE)},a.Zb=function(t){for(var e=[],n=0;n<t.length;n++){var r=t[n].pattern;if("string"==typeof r)try{e.push(new RegExp(r))}catch(t){M.exception(t,"Parse regex pattern failed.")}else M.error("xhr filter pattern should be a string")}return e},a.fd=function(t,e,n){var r=n&&n.include;return n=n&&n.exclude,r&&0<r.length&&!a.Cc(e,t,r)||n&&0<n.length&&a.Cc(e,t,n)},a.dc=function(t){var e=t.message||t.description,n=t.fileName||t.filename,r=t.lineNumber;M.utils.isString(t.description)&&0<=t.description.indexOf("Access is denied.")&&(e+=": maybe you have CORS XHR error in IE"),M.monitor.Fa.Uc(e,n,r,t)},a.prototype.setUp=function(){if(this.ab){M.log("M29"),M.xhrConstructor=window.XMLHttpRequest,M.xhrOpen=this.xhrOpen=this.d.open,M.xhrSend=this.xhrSend=this.d.send;var i=this;this.d.open=M.aop.around(this.d.open,function(){var t=1<=arguments.length?String(arguments[0]):"",e=2<=arguments.length?String(arguments[1]):"";e=M.utils.getFullyQualifiedUrl(e),i.xa>=i.conf.maxPerPageView||a.fd(e,t,i.conf)||(this._adrumAjaxT=new M.events.AdrumAjax(M.utils.mergeJSON({method:t,url:e,xhr:this},i.status)))},null,"XHR.open",a.dc),this.d.send=M.aop.around(this.d.send,function(){var n=this,t=n._adrumAjaxT;if(t&&!(++i.xa>i.conf.maxPerPageView)){var e=M.utils.now(),r=t.getSendTime();M.assert(null===r,"M30"),t.timestamp(e),t.markSendTime(r||e),t.parentPhase(M.lifecycle.getPhaseName()),a.fg(t.url())?n.setRequestHeader("ADRUM","isAjax:true"):M.log("M31",document.location.href,t.url());var o=0;!function t(){if(4==n.readyState)M.log("M32"),i.ta(n);else{var e=null;try{e=n.onreadystatechange}catch(t){return M.log("M33",t),void i.ta(n)}o++,e?M.aop.support(e)?(n.onreadystatechange=i.$b(e,n,"XHR.onReadyStateChange"),M.log("M34",o)):(M.log("M35"),i.ta(n)):o<a.Le?M.utils.Xa(t):(M.log("M36"),i.ta(n))}}()}},null,"XHR.send",a.dc),"addEventListener"in this.d&&"removeEventListener"in this.d&&M.aop.support(this.d.addEventListener)&&M.aop.support(this.d.removeEventListener)?(this.d.addEventListener=M.aop.around(this.d.addEventListener,this.ff(),null,"XHR.addEventListener"),this.d.removeEventListener=M.aop.around(this.d.removeEventListener,function(t,e){if(this._adrumAjaxT){var n=Array.prototype.slice.call(arguments);return e.__adrumInterceptor?(n[1]=e.__adrumInterceptor,M.log("M37")):M.log("M38"),n}},null,"XHR.removeEventListener")):M.log("M39"),M.log("M40")}},a.prototype.Jg=function(){this.xa=0},a.rg=function(t,e){for(var n=!1,r=0;r<e.length;r++){var o=e[r];if(o&&o.test(t)){n=!0;break}}return n},a.Cc=function(t,e,n){var r=!1;if(e&&n)for(var o=0;o<n.length;o++){var i=n[o];if(!(i.method&&t!==i.method||i.urls&&!a.rg(e,i.urls))){r=!0;break}}return r},a.Fg=function(t,e,n){return(e||t)===(n||t)},a.tc=function(t){var e=t._adrumAjaxT;if(e){var n=(new Date).getTime();2==t.readyState?e.markFirstByteTime(e.getFirstByteTime()||n):4==t.readyState&&(M.assert(null===e.getRespAvailTime(),"M41"),e.markRespAvailTime(e.getRespAvailTime()||n),e.markFirstByteTime(e.getFirstByteTime()||n))}},a.fg=function(t){var e=document.createElement("a");e.href=t;var n=(t=document.location).protocol;return e.protocol===n&&e.hostname===t.hostname&&a.Fg(a.jf[n],e.port,t.port)},a.prototype.$b=function(t,n,e){return a.rh(t,function(){a.tc(this)},function(){var t=n._adrumAjaxT;if(t&&4==n.readyState){var e=(new Date).getTime();M.assert(null===t.getRespProcTime(),"M42"),t.markRespProcTime(t.getRespProcTime()||e),a.a(n,t)}},e)},a.a=function(t,e){var n=t.status;if(400<=n){var r=t.responseText;e.error({status:n,msg:M.utils.isString(r)?r:""})}M.command("reportXhr",e)},a.prototype.ta=function(r){if(r._adrumAjaxT){var o=(new Date).getTime()+3e4;!function t(){a.tc(r);var e=r._adrumAjaxT;if(e){var n=(new Date).getTime();4==r.readyState?(M.assert(null===e.getRespProcTime(),"M43"),e.markRespProcTime(e.markRespProcTime()||n),M.log("M44"),a.a(r,e),delete r._adrumAjaxT):n<o?setTimeout(t,a.qb):(delete r._adrumAjaxT,M.log("M45"))}}()}},a.rh=function(t,e,n,r){var o=t;return t&&"object"===(void 0===t?"undefined":_typeof(t))&&"toString"in t&&"[xpconnect wrapped nsIDOMEventListener]"===t.toString()&&"handleEvent"in t&&(o=function(){t.handleEvent.apply(this,Array.prototype.slice.call(arguments))}),M.aop.around(o,e,n,r)},a.prototype.ff=function(){for(var t=0;t<arguments.length;t++);var o=this;return function(t,e){if(("load"===t||"error"===t)&&e&&this._adrumAjaxT){var n;if((n=e).__adrumInterceptor)n=n.__adrumInterceptor;else if(M.aop.support(n)){var r=o.$b(n,this,"XHR.invokeEventListener");n=n.__adrumInterceptor=r}else n=null;if(n)return(r=Array.prototype.slice.call(arguments))[1]=n,M.log("M46"),r;M.log("M47",t,e)}}},a.Le=5,a.qb=50,a.jf={"http:":"80","https:":"443"},a}(A.rb),A.ea=C,A.ua=new A.ea,function(u){function c(t,e){var n=[];if(o=/^\s*(ADRUM_BT\w*)=(.*)\s*$/i.exec(t)){var r=o[1],o=o[2].replace(/^"|"$/g,""),i=(o=decodeURIComponent(o).split("|"))[0].split(":");if("R"===i[0]&&Number(i[1])===e)for(a(r),r=1;r<o.length;r++)n.push(o[r])}return n}function f(t,e){var n=/^\s*(ADRUM_(\d+)_(\d+)_(\d+))=(.*)\s*$/i.exec(t);if(n){var r=n[1],o=n[4],i=n[5];if(Number(n[3])===e)return a(r),{index:Number(o),value:i}}return null}function l(t){var e=/^\s*ADRUM=s=([\d]+)&r=(.*)\s*/.exec(t);if(e)return R.log("M50",t),3===e.length?(a("ADRUM"),{startTime:Number(e[1]),startPage:e[2]}):(R.error("M51",t),null)}function a(t){R.log("M49",t);var e=new Date;e.setTime(e.getTime()-1e3),document.cookie=t+"=;Expires="+e.toUTCString()}u.startTimeCookie=null,u.cookieMetadataChunks=null,u.bc=function(t,e){R.log("M48");for(var n=e?e.length:0,r=[],o=t.split(";"),i=0;i<o.length;i++){var a=o[i],s=f(a,n);s?r.push(s):null!=(a=l(a))&&(u.startTimeCookie=a)}for(Array.prototype.sort.call(r,function(t,e){return t.index-e.index}),a=[],i=0;i<r.length;i++)a.push(r[i].value);for(i=0;i<o.length;i++)(r=c(o[i],n))&&0<r.length&&(a=a.concat(r));u.cookieMetadataChunks=a},R.correlation.eck=u.bc}((R=t||(t={})).correlation||(R.correlation={})),(S=t||(t={})).report=function(t){S.utils.Xa(function(){S.command("reportEvent",t)})},"APP_KEY_NOT_SET"===(x=t||(t={})).conf.appKey&&"undefined"!=typeof console&&void 0!==console.log&&console.log("AppDynamics EUM cloud application key missing. Please specify window['adrum-app-key']"),x.correlation.bc(document.cookie,document.referrer),x.command("mark","firstbyte",window["adrum-start-time"]),x.monitor.ed(x.monitor.Fa,x.monitor.lf,x.monitor.perfMonitor,x.monitor.ua),(E=(E=(E=t||(t={})).ng||(E.ng={})).c||(E.c={})).Gc="locationChangeStart",E.og="locationChangeSuccess",E.$c="routeChangeStart",E.ad="routeChangeSuccess",E.hd="stateChangeStart",E.jd="stateChangeSuccess",E.rd="viewContentLoaded",E.Qf="includeContentRequested",E.Pf="includeContentLoaded",E.ac="digest",E.Uh="outstandingRequestsComplete",E.Ub="beforeNgXhrRequested",E.Mb="afterNgXhrRequested",E.Th="ngXhrLoaded",E.Xb="$$completeOutstandingRequest",function(l){function a(e,t,n,r,o,i){if(t)try{return t.apply(e,[n,r,o].concat(i))}catch(t){return e.error(n,r,o,i,l.Error.Sd,"an exception occurred in a caller-provided callback function",t)}}function p(o,i){return function(){var t=this.current,e=i[t]||i[l.da]||t,n=Array.prototype.slice.call(arguments);if(this.af(o))return this.error(o,t,e,n,l.Error.Td,"event "+o+" inappropriate in current state "+this.current);if(!1===a(this,this["onbefore"+o],o,t,e,n))return l.ca.nb;if(e===l.da&&(e=t),t===e)return a(this,this["onafter"+o]||this["on"+o],o,t,e,n),l.ca.we;var r=this;return!(this.transition=function(){return r.transition=null,r.current=e,a(r,r["onenter"+e]||r["on"+e],o,t,e,n),a(r,r["onafter"+o]||r["on"+o],o,t,e,n),l.ca.Ee})===a(this,this["onleave"+t],o,t,e,n)?(this.transition=null,l.ca.nb):this.transition?this.transition():void 0}}var d=T.utils.hasOwnPropertyDefined;l.VERSION="2.3.5",l.ca={Ee:1,we:2,nb:3,wh:4},l.Error={Td:100,xh:200,Sd:300},l.da="*",l.create=function(t,e){function n(t){var e=t.from instanceof Array?t.from:t.from?[t.from]:[l.da];s[t.name]=s[t.name]||{};for(var n=0;n<e.length;n++)u[e[n]]=u[e[n]]||[],u[e[n]].push(t.name),s[t.name][e[n]]=t.to||e[n]}var r="string"==typeof t.initial?{state:t.initial}:t.initial,o=e||t.target||{},i=t.events||[],a=t.callbacks||{},s={},u={};r&&(r.event=r.event||"startup",n({name:r.event,from:"none",to:r.state}));for(var c=0;c<i.length;c++)n(i[c]);for(var f in s)d(s,f)&&(o[f]=p(f,s[f]));for(f in a)d(a,f)&&(o[f]=a[f]);return o.current="none",o.Nh=function(t){return t instanceof Array?0<=t.indexOf(this.current):this.current===t},o.$e=function(t){return!this.transition&&(d(s[t],this.current)||d(s[t],l.da))},o.af=function(t){return!this.$e(t)},o.sa=function(){return u[this.current]},o.error=t.error||function(t,e,n,r,o,i,a){throw a||i},r&&!r.defer&&o[r.event](),o}}((T=t||(t={})).Gb||(T.Gb={})),y=t||(t={}),b=y.events||(y.events={}),w=function(e){function t(t){e.call(this,t),this.perf=new y.PerformanceTracker,this.start()}return n(t,e),t.prototype.type=function(){return 3},t.prototype.Ff=function(){return b.EventTracker.Rb(this.guid(),this.url(),this.type())},t.prototype.gd=function(t){var e=this.Ff();t.set("parent",e),y.log("M52",e.guid(),e.url())},t.prototype.startCorrelatingXhrs=function(){y.log("M53"),this.gd(y.monitor.ua)},t.prototype.stopCorrelatingXhrs=function(){y.monitor.ua.set("parent",null),y.log("M54")},t.prototype.Xg=function(){y.log("M55"),this.gd(y.monitor.Fa)},t.prototype.start=function(){this.markVirtualPageStart(),this.startCorrelatingXhrs()},t.prototype.end=function(){this.markVirtualPageEnd(),this.stopCorrelatingXhrs()},t}(b.EventTracker),b.VPageView=w,b.V(b.l[3],w.prototype),b.Sb(b.B[3],w.prototype),g=t||(t={}),(v=(v=g.ng||(g.ng={})).conf||(v.conf={})).disabled=g.conf.userConf&&g.conf.userConf.spa&&g.conf.userConf.spa.angular&&g.conf.userConf.spa.angular.disable,v.ha=!!(g.conf.userConf&&g.conf.userConf.spa&&g.conf.userConf.spa.angular&&!0===g.conf.userConf.spa.angular.ha),v.xhr={},v.metrics={includeResTimingInEndUserResponseTiming:!0},g.conf.userConf&&g.conf.userConf.spa&&g.conf.userConf.spa.angular&&g.conf.userConf.spa.angular.vp&&(g.conf.userConf.spa.angular.vp.xhr&&g.monitor.ea.Rc(v.xhr,g.conf.userConf.spa.angular.vp.xhr),g.conf.userConf.spa.angular.vp.metrics&&g.utils.mergeJSON(v.metrics,g.conf.userConf.spa.angular.vp.metrics)),d=t||(t={}),h=d.ng||(d.ng={}),m=function(e){function s(t){e.call(this,t),this.Ac=!0,this.X={},this.T=0,this.stopCorrelatingXhrs()}return n(s,e),s.prototype.type=function(){return 3},s.prototype.lb=function(){this.markViewChangeStart(),this.markVirtualPageStart(this.getViewChangeStart()),this.timestamp(this.getViewChangeStart())},s.prototype.Rf=function(){this.digestCount(this.digestCount()+1)},s.prototype.Sf=function(){this.T++,d.log("increasing xhr count "+this.T+" pending xhr requests")},s.prototype.hf=function(){this.T--,d.log("decreasing xhr count "+this.T+" pending xhr requests")},s.prototype.Mf=function(){var t=this.perf.getEntryByName(d.events.b.wd);return d.log("xhrCount "+this.T+" xhrReuqestCompleted "+t),0<this.T},s.prototype.Xe=function(){var t={ra:0},e=document.querySelectorAll("ng-view, [ng-view], .ng-view, [ui-view]");if(e&&0<e.length)for(var n in s.Xc)for(var r=0;r<e.length;r++){var o=angular.element(e[r]).find(n);if(0<o.length)for(var i=0;i<o.length;i++){var a=o[i][s.Xc[n].cb];(a=a?decodeURIComponent(a):null)&&!t[a]&&(t[a]=n,t.ra++)}}this.X=t},s.prototype.We=function(t){return!!this.X[decodeURIComponent(t.name)]},s.prototype.Ye=function(){var t=[],e=this;0<this.X.ra&&(t=d.monitor.perfMonitor.nc().filter(function(t){return e.We(t)})),this.resTiming(t)},s.uf=function(t){for(var e=[],n=0;n<t.length;n++){var r=t[n];2!==t[n].eventType&&101!==t[n].eventType||d.monitor.ea.fd(r.eventUrl,r.method,h.conf.xhr)||e.push(t[n])}return e},s.Gf=function(t){var e,n,r=-1;for(e=0,n=t.length;e<n;e++)r=Math.max(r,t[e].timestamp+t[e].metrics.PLT);return r},s.prototype.Re=function(){if(h.conf.xhr){var t=s.uf(d.channel.getEventsWithParentGUID(this.guid()));if(0<(t=s.Gf(t))){var e=this.perf.getEntryByName(d.events.b.wd);this.markXhrRequestsCompleted(Math.min(e&&e.startTime||Number.MAX_VALUE,t))}}},s.prototype.adjustTimings=function(){this.Re();var t=this.getViewDOMLoaded(),e=this.getXhrRequestsCompleted();t=Math.max(t,e),h.conf.metrics.includeResTimingInEndUserResponseTiming&&(this.Qe(),e=this.getViewResourcesLoaded(),e=Math.max(t,e),d.log("adjust this.end from %s to %s",t,e),t=e),this.markVirtualPageEnd(t)},s.prototype.Qe=function(){if(0<this.X.ra){this.Ye();var t=this.resTiming();if(t&&t.length>=this.X.ra){for(var e=[],n=0;n<t.length;n++)e.push(t[n].responseEnd);t=Math.max.apply(Math,e),this.markViewResourcesLoaded(d.PerformanceTracker.Aa(t))}}},s.prototype.identifier=function(t){var e=this.td;return d.utils.isDefined(t)&&(this.td=s.tf(t),this.url(this.td.url)),e},s.tf=function(t){var e={};return t&&t.g?(e.g={Pa:""},d.utils.mergeJSON(e.g,{Pa:t.g.originalPath,Y:t.g.template,Z:t.g.templateUrl})):t&&t.state&&(e.state={url:""},d.utils.mergeJSON(e.state,{url:t.state.url,name:t.state.name,Y:t.state.template,Z:t.state.templateUrl})),e},s.Xc={img:{cb:"src"},script:{cb:"src"},link:{cb:"href"}},s}(d.events.VPageView),h.NgVPageView=m,d.events.V(d.events.l[102],m.prototype),f=t||(t={}),l=f.ng||(f.ng={}),p=function(){function e(){this.e=new l.NgVPageView}return e.prototype.Ng=function(){var t=this;l.conf.metrics.includeResTimingInEndUserResponseTiming?(f.log("M56"),setTimeout(function(){t.Ta()},e.Ge)):setTimeout(function(){t.Ta()},e.He)},e.prototype.Ta=function(){f.log("M57");var t=this.e;f.command("call",function(){t.adjustTimings(),f.reporter.reportEvent(t)})},e.prototype.Sg=function(t){this.e=t},e.Ge=5e3,e.He=2*f.monitor.ea.qb,e}(),l.VirtualPageStateMachine=p,f.Gb.create({events:[{name:"start",from:"none",to:"ChangeView"},{name:"viewLoaded",from:"ChangeView",to:"XhrPending"},{name:"xhrCompleted",from:"XhrPending",to:"End"},{name:"abort",from:"*",to:"none"},{name:"init",from:"*",to:"none"},{name:"locChange",from:"*",to:"*"},{name:"beforeXhrReq",from:"*",to:"*"},{name:"afterXhrReq",from:"*",to:"*"}],error:function(t){f.log("M58"+t)},callbacks:{onChangeView:function(){this.e.lb(),this.e.Xg()},onviewLoaded:function(){this.e.markViewDOMLoaded()},onXhrPending:function(){this.e.Ac&&this.xhrCompleted()},onleaveXhrPending:function(t,e,n){return"abort"===t?(this.Ta(),!0):"xhrCompleted"===t&&"End"===n?!this.e.Mf()&&(this.e.markXhrRequestsCompleted(),!0):void 0},onEnd:function(){this.e.Xe(),this.Ng()},oninit:function(t,e,n,r){this.Sg(r),f.monitor.ua.Jg()},onlocChange:function(t,e,n,r){this.e.identifier.url=r},onbeforeXhrReq:function(t,e,n,r){var o=this.e;return o.Ac=!1,f.log("M59",r&&r[1]||"",o.guid()),o.Sf(),o.startCorrelatingXhrs(),r[3]&&(r[3]=f.aop.before(r[3],function(t,e,n){f.log("M60"),o.hf(),n&&(t=f.utils.Eg(n)["content-type"])&&0<=t.indexOf("text/html")&&o.markViewFragmentsLoaded()})),r},onafterXhrReq:function(){this.e.stopCorrelatingXhrs()}}},p.prototype),s=t||(t={}),u=s.ng||(s.ng={}),c=function(){function r(){this.k=new u.VirtualPageStateMachine,this.ha=s.ng.conf.ha}return r.prototype.h=function(t,e){switch(s.log("M61",t),t){case u.c.$c:case u.c.hd:this.k.start();var n=new u.NgVPageView({url:e.next.url,identifier:e.next});this.ha&&r.$f(this.k.e,n)?this.k.e.dd({url:e.next.url,identifier:e.next}):this.bh(n);break;case u.c.ad:case u.c.jd:this.k.e.markViewChangeEnd();break;case u.c.rd:this.k.viewLoaded();break;case u.c.Ub:this.k.beforeXhrReq(e);break;case u.c.Mb:this.k.afterXhrReq();break;case u.c.Xb:this.k.xhrCompleted();break;case u.c.Gc:this.k.locChange(e.next.url);break;case u.c.ac:this.k.e.Rf()}},r.prototype.bh=function(t){this.k.abort(),this.k.init(t),this.k.start()},r.$f=function(t,e){var n=t.identifier(),r=e.identifier();return!((s.utils.isDefined(n)||s.utils.isDefined(r))&&n!==r&&(!s.utils.isDefined(n)||!s.utils.isDefined(r)||(n.state||r.state?!s.utils.isDefined(n.state)||!s.utils.isDefined(r.state)||n.state.name!==r.state.name||n.state.Y!==r.state.Y||n.state.Z!==r.state.Z||n.state.url!==r.state.url:n.g&&r.g?n.g.Pa!==r.g.Pa||n.g.Y!==r.g.Y||n.g.Z!==r.g.Z:n.url!==r.url)))},r}(),u.Je=c,i=t||(t={}),a=i.ng||(i.ng={}),o=function(){function t(){this.j=new a.Je}return t.prototype.setUp=function(){var t=this;i.utils.addEventListener(document,"DOMContentLoaded",function(){i.log("M62"),t.init()})},t.prototype.init=function(){if("undefined"!=typeof angular){i.log("M63");var e=this,t=angular.module("ng");t.config(["$provide",function(t){e.Xf(t),e.Wf(t)}]),t.run(["$browser",function(t){e.Vf(t)}]),i.log("M64")}},t.prototype.Wf=function(t){var e=i.aop,n=this;t.decorator("$httpBackend",["$delegate",function(t){return e.around(t,function(){var t=Array.prototype.slice.call(arguments);return n.j.h(a.c.Ub,t),t},function(){n.j.h(a.c.Mb)})}])},t.prototype.Xf=function(t){var e=i.aop,o=this;t.decorator("$rootScope",["$delegate",function(t){return t.$digest=e.after(t.$digest,function(){o.j.h(a.c.ac)}),t.$on("$locationChangeStart",function(t,e){var n={url:e},r=t&&t.W&&t.W.$state&&t.W.$state.current;r&&(n.state=r),o.j.h(a.c.Gc,{next:n})}),t.$on("$locationChangeSuccess",function(){o.j.h(a.c.og)}),t.$on("$routeChangeStart",function(t,e){var n={url:location.href},r=e&&e.$$route;r&&(n.g=r),o.j.h(a.c.$c,{next:n})}),t.$on("$routeChangeSuccess",function(){o.j.h(a.c.ad)}),t.$on("$stateChangeStart",function(t,e){o.j.h(a.c.hd,{next:{state:e}})}),t.$on("$stateChangeSuccess",function(){o.j.h(a.c.jd)}),t.$on("$viewContentLoaded",function(t){var e={url:location.href};(t=t&&t.W&&t.W.$state&&t.W.$state.current)&&(e.state=t),o.j.h(a.c.rd,{next:e})}),t.$on("$includeContentRequested",function(){o.j.h(a.c.Qf)}),t.$on("$includeContentLoaded",function(){o.j.h(a.c.Pf)}),t}])},t.prototype.Vf=function(t){var e=this;t.$$completeOutstandingRequest=i.aop.before(t.$$completeOutstandingRequest,function(){e.j.h(a.c.Xb)})},t}(),a.sh=o,a.ngMonitor=new o,e=t||(t={}),(r=e.ng||(e.ng={})).conf.disabled||e.monitor.ed(r.ngMonitor)}var e,r,i,a,o,s,u,c,f,l,p,d,h,m,g,v,y,b,w,T,E,x,S,R,M,A,C,k,P,L,D,U,X,_,j,V,$,N,O,I,B,q,F,G,H,Z,Q,Y,J,W,K,z,tt,et,nt,rt,ot,it,at,st,ut,ct,ft,lt,pt,dt,ht,mt,gt,vt,yt,bt,wt,Tt,Et,xt};