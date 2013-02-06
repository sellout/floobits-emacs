import os

import utils


class CloudAgent():
    CLOUD_VERSION = "0.01"

    def sendToCloud(self, req):
        raise NotImplemented('')

    def cloud_room_info(self, req):
        self.perms = req['perms']
        self.tree = req['tree']
        self.projectPath = utils.unfuck_path(os.path.abspath('./shared'))
        self.sendToEditor(req)
        self.readOnly = True

        if 'patch' not in self.perms:
            print("We don't have patch permission. Setting buffers to read-only")
            self.readOnly = True

        self.basePath = os.path.join(self.projectPath, self.room_owner, self.room)
        print('making dir', self.basePath)
        utils.mkdir(self.basePath)

        self.bufs = {}
        for bufId, buf in req['bufs'].iteritems():
            bufId = int(bufId)  # json keys must be strings
            self.bufs[bufId] = buf
            newDir = os.path.split(os.path.join(self.basePath, buf['path']))[0]
            utils.mkdir(newDir)
            self.sendToCloud({
                'name': 'get_buf',
                'id': bufId,
            })

        print('Successfully joined room %s/%s' % (self.room_owner, self.room))

    def cloud_patch(self, req):
        pass

    def cloud_get_buf(self, req):
        bufId = req['id']
        self.bufs[bufId] = req
        filePath = os.path.join(self.basePath, req['path'])
        with open(filePath, 'w') as fd:
            fd.write(req['buf'])
        self.bufs[bufId]['full_path'] = filePath
        print('got buf %s. buf is now %s' % (bufId, self.bufs[bufId]))
        req['full_path'] = filePath
        self.sendToEditor(req)
        del self.bufs[bufId]['name']

    def cloud_create_buf(self, req):
        pass

    def cloud_rename_buf(self, req):
        pass

    def cloud_delete_buf(self, req):
        pass

    def cloud_join(self, req):
        pass

    def cloud_part(self, req):
        pass

    def cloud_highlight(self, req):
        pass

    def cloud_error(self, req):
        pass

    def cloud_disconnect(self, req):
        self.cloudFactory.reconnect = False
        self.sendToEditor(req)
        print('diconnected: ', req)

    def cloud_msg(self):
        pass
