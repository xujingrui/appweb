#encoding: utf-8
import requests



def DockerStatus(items):
    alldata =[]
    for line in items:
        url = 'http://%s:%s/containers/json' % (line.hostipaddr, line.hostport)
        r = requests.get(url)
        data = r.json()
        datalist = []
        for i in data:
            datalist.append(i['Names'][0].strip('/'))
        containers = []
        for j in datalist:
            url = 'http://%s:%s/containers/%s/stats?stream=false' % (line.hostipaddr, line.hostport,j)
            r = requests.get(url)
            data = r.json()
            cpu_total_usage = data['cpu_stats']['cpu_usage']['total_usage']
            pre_cpu_total_usage = data['precpu_stats']['cpu_usage']['total_usage']
            cpu_delta = cpu_total_usage - pre_cpu_total_usage
            system_usage = data['cpu_stats']['system_cpu_usage']
            pre_system_usage = data['precpu_stats']['system_cpu_usage']
            system_delta = system_usage - pre_system_usage
            length = len(data['precpu_stats']['cpu_usage']['percpu_usage'])
            udata = ((float(cpu_delta) / system_delta) * length) * 100.0
            CPU = round(udata, 2)
            menusage = data['memory_stats']['usage'] / 1024000
            menlimit = data['memory_stats']['limit'] / 1024000
            MEN = round((float(menusage) / menlimit) * 100.0, 2)
            PID = data['pids_stats']['current']
            neti = data['networks']['eth0']['rx_bytes'] / 1024
            neto = data['networks']['eth0']['tx_bytes'] / 1024
            name = data['name'].strip('/')
            #print 'NAME', name, '     CPU ', CPU, '%', '     MEN ', MEN, '%     ', menusage, 'MB', menlimit, 'MB', '     NET_I ', neti, 'KB', '     NET_O ', neto, 'KB', '     PID', PID
            containers.append({
                "container_name": j,
                "container_CPU": CPU,
                "container_MEN": MEN,
                "container_menusage": menusage,
                "container_menlimit": menlimit,
                "container_neti": neti,
                "container_neto": neto,
                "container_PID": PID})
        alldata.append({"hostname": line.hostname, "hostipaddr": line.hostipaddr, "hostport": line.hostport, "containers": containers})
        #print(json.dumps(alldata, indent=1))
    return alldata














if __name__ == '__main__':
    DockerStatus('[1,2,3,4,5,]')