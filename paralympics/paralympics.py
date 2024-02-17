'''
from flask import current_app as app
@app.route('/')
def hello():
    return f"Hello!"
'''


from flask import Blueprint, request, jsonify
from . import db, ma
from .models import Event, Region
from .schemas import EventSchema, RegionSchema

bp = Blueprint('paralympics', __name__)

# Flask-Marshmallow Schemas
regions_schema = RegionSchema(many=True)
region_schema = RegionSchema()
events_schema = EventSchema(many=True)
event_schema = EventSchema()

@bp.route("/regions", methods=["GET"])
def get_regions():
    all_regions = Region.query.all()
    result = regions_schema.dump(all_regions)
    return jsonify(result)

@bp.route("/regions/<NOC>", methods=["GET"])
def get_region(NOC):
    region = Region.query.get_or_404(NOC)
    return region_schema.jsonify(region)

@bp.route("/regions", methods=["POST"])
def add_region():
    new_region = region_schema.load(request.json, session=db.session)
    db.session.add(new_region)
    db.session.commit()
    return region_schema.jsonify(new_region), 201

@bp.route("/regions/<NOC>", methods=["PATCH"])
def update_region(NOC):
    region = Region.query.get_or_404(NOC)
    region_schema.load(request.json, instance=region, session=db.session, partial=True)
    db.session.commit()
    return region_schema.jsonify(region)

@bp.route("/regions/<NOC>", methods=["DELETE"])
def delete_region(NOC):
    region = Region.query.get_or_404(NOC)
    db.session.delete(region)
    db.session.commit()
    return jsonify({"message": f"Region {NOC} successfully deleted."}), 202

@bp.route("/events", methods=["GET"])
def get_events():
    all_events = Event.query.all()
    result = events_schema.dump(all_events)
    return jsonify(result)

@bp.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    return event_schema.jsonify(event)

@bp.route("/events", methods=["POST"])
def add_event():
    new_event = event_schema.load(request.json, session=db.session)
    db.session.add(new_event)
    db.session.commit()
    return event_schema.jsonify(new_event), 201

@bp.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    event_schema.load(request.json, instance=event, session=db.session, partial=True)
    db.session.commit()
    return event_schema.jsonify(event)

@bp.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": f"Event {event_id} successfully deleted."}), 202
