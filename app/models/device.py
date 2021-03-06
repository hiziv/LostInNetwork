# -*- coding: utf-8 -*-

from datetime import datetime

from app import app, db
from app.utils.crypto import PasswordManager


class DeviceInterfaces(db.Model):
    """
    List all interfaces from network device.
    Link to configuration table with configuration_id
    One entry per interfaces
    """

    friendly_name = "Device Interfaces"
    __tablename__ = "deviceinterfaces"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    addr = db.Column(db.String())
    netmask = db.Column(db.String())
    configuration_id = db.Column(db.Integer, db.ForeignKey('configuration.id'))

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error("Error during save operation {}".format(e))
            app.logger.exception()
            db.session.rollback()
            return False
        return True

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error("Error during delete operation {}".format(e))
            app.logger.exception()
            db.session.rollback()
            return False
        return True

    def __repr__(self):
        return self.name


class DeviceRoutes(db.Model):
    """
    Represent all routes for e device
    link to configuration with configuration_id
    """

    friendly_name = "Device Routes"
    __tablename__ = "deviceroutes"

    id = db.Column(db.Integer(), primary_key=True)
    net_dst = db.Column(db.String())
    net_mask = db.Column(db.String())
    gw = db.Column(db.String())
    connected = db.Column(db.Enum('0', '1'))
    configuration_id = db.Column(db.Integer(), db.ForeignKey(
        'configuration.id'))

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error("Error during save operation {}".format(e))
            app.logger.exception()
            db.session.rollback()
            return False
        return True

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error("Error during delete operation {}".format(e))
            app.logger.exception()
            db.session.rollback()
            return False
        return True

    def __repr__(self):
        return self.name


class DeviceType(db.Model):
    """
    Represents the Type of a Device.
    Contains FK to a Manufacturer and a DeviceTypeCategory.
    """
    friendly_name = "Device Type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'))
    category = db.Column(db.Enum('Router', 'Level 2 Switch', 'Level 3 Switch',
                                 'Firewall', name='type'), default='Router')

    devices = db.relationship('Device', backref='devicetype', lazy='dynamic')

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error("Error during save operation {}".format(e))
            app.logger.exception()
            db.session.rollback()
            return False
        return True

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error("Error during delete operation {}".format(e))
            app.logger.exception()
            db.session.rollback()
            return False
        return True

    def __repr__(self):
        return self.name


# Many to Manu Relationship between Risk and Device
# A Device can be associated with many risks
# A Risk can be associated with many devices
device_risks = db.Table(
    'device_risks',
    db.Column('device_id', db.Integer, db.ForeignKey('device.id')),
    db.Column('risk_id', db.Integer, db.ForeignKey('risk.id')),
)


class Device(db.Model):
    """
    Represents a Device, associated with a DeviceType, a Lan and a Configuration.
    A Device also has Risks associated to it.
    """
    friendly_name = "Device"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    ip = db.Column(db.String(50))
    date = db.Column(db.DateTime())
    username = db.Column(db.String(50), default='root')
    password = db.Column(db.String(66))
    enausername = db.Column(db.String(50))
    enapassword = db.Column(db.String(66))
    method = db.Column(db.Enum('ssh', 'telnet', 'scp', name='connect_method'),
                       default='ssh')
    status = db.Column(db.Integer)
    lan_id = db.Column(db.Integer, db.ForeignKey('lan.id'))
    configurations = db.relationship('Configuration', backref='device', lazy='dynamic')
    devicetype_id = db.Column(db.Integer, db.ForeignKey('device_type.id'))

    risks = db.relationship('Risk', secondary=device_risks,
                            backref=db.backref('pages', lazy='dynamic'))

    def decrypt_password(self):
        return PasswordManager.decrypt_string_from_session_pwdh(self.password)

    def decrypt_enapassword(self):
        return PasswordManager.decrypt_string_from_session_pwdh(self.enapassword)

    def save(self, encrypt=True):
        self.date = datetime.now()
        if encrypt:
            self.password = PasswordManager.encrypt_string_from_session_pwdh(self.password)
            self.enapassword = PasswordManager.encrypt_string_from_session_pwdh(self.enapassword)
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error("Error during save operation {}".format(e))
            app.logger.exception()
            db.session.rollback()
            return False
        return True

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error("Error during delete operation {}".format(e))
            app.logger.exception()
            db.session.rollback()
            return False
        return True

    def __repr__(self):
        return self.name
