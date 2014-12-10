# -*- coding: utf-8 -*-

from app import db


class DeviceTypeCategory(db.Model):
    """
    Represents the Category of a DeviceType
    Example : Firewall, Router, etc...
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    devicetypes = db.relationship('DeviceType', backref='devicetypecategory', lazy='dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return self.name


class DeviceType(db.Model):
    """
    Represents the Type of a Device.
    Contains FK to a Manufacturer and a DeviceTypeCategory.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'))
    devicetypecategory_id = db.Column(db.Integer, db.ForeignKey('device_type_category.id'))

    devices = db.relationship('Device', backref='devicetype', lazy='dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    ip1 = db.Column(db.String(50))
    ip2 = db.Column(db.String(50))
    date = db.Column(db.DateTime())

    lan_id = db.Column(db.Integer, db.ForeignKey('lan.id'))
    configuration_id = db.Column(db.Integer, db.ForeignKey('configuration.id'))
    devicetype_id = db.Column(db.Integer, db.ForeignKey('device_type.id'))

    risks = db.relationship('Risk', secondary=device_risks, backref=db.backref('pages', lazy='dynamic'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return self.name

