from django.shortcuts import render

# Create your views here.

def home(request) :
  return  render(request, "Setup.html", {})

def batch(request) :
  return  render(request, "Batch.html", {})


def group(request) :
  return  render(request, "group.html", {})


def visualization(request) :
  return  render(request, "visualization.html", {})